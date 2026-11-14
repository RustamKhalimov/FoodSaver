from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from accounts.models import UserProfile

from .models import DiscountRule, Order, Product


class ProductAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.today = timezone.localdate()
        self.customer = self.create_user('customer')
        self.admin = self.create_user('admin', UserProfile.ROLE_ADMIN)

    def create_user(self, username, role=UserProfile.ROLE_CUSTOMER):
        from django.contrib.auth.models import User

        user = User.objects.create_user(
            username=username,
            email=f'{username}@example.com',
            password='StrongPass123!xyz',
        )
        user.profile.role = role
        user.profile.save()
        return user

    def test_only_admin_can_create_update_and_delete_products(self):
        existing_product = Product.objects.create(
            name='Existing Product',
            quantity=5,
        )
        self.client.force_authenticate(user=self.customer)
        customer_response = self.client.post(
            '/api/products/',
            {
                'name': 'Customer Product',
                'quantity': 5,
            },
            format='json',
        )
        self.assertEqual(customer_response.status_code, 403)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(
            self.client.patch(
                f'/api/products/{existing_product.pk}/',
                {'quantity': 8},
                format='json',
            ).status_code,
            403,
        )
        self.assertEqual(
            self.client.delete(
                f'/api/products/{existing_product.pk}/'
            ).status_code,
            403,
        )

        self.client.force_authenticate(user=self.admin)
        admin_response = self.client.post(
            '/api/products/',
            {
                'name': 'Admin Product',
                'quantity': 5,
            },
            format='json',
        )
        self.assertEqual(admin_response.status_code, 201)
        product_id = admin_response.data['id']

        update_response = self.client.patch(
            f'/api/products/{product_id}/',
            {'quantity': 8},
            format='json',
        )
        self.assertEqual(update_response.status_code, 200)

        delete_response = self.client.delete(f'/api/products/{product_id}/')
        self.assertEqual(delete_response.status_code, 204)

    def test_customers_can_browse_catalog_and_expiring_products(self):
        Product.objects.create(
            name='Milk',
            expiry_date=self.today + timedelta(days=2),
            quantity=5,
        )

        self.client.force_authenticate(user=self.customer)
        self.assertEqual(self.client.get('/api/products/').status_code, 200)
        self.assertEqual(
            self.client.get('/api/products/expiring/').status_code,
            200,
        )

    def test_customer_catalog_excludes_expired_and_unavailable_products(self):
        Product.objects.create(
            name='Available',
            expiry_date=self.today,
            quantity=1,
        )
        Product.objects.create(
            name='Expired',
            expiry_date=self.today - timedelta(days=1),
            quantity=4,
        )
        Product.objects.create(
            name='Out of stock',
            expiry_date=self.today + timedelta(days=1),
            quantity=0,
        )
        self.client.force_authenticate(user=self.customer)

        response = self.client.get('/api/products/catalog/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual([item['name'] for item in response.data], ['Available'])

    def test_customer_can_place_order_with_server_calculated_discount(self):
        product = Product.objects.create(
            name='Discounted Milk',
            expiry_date=self.today + timedelta(days=1),
            quantity=3,
            regular_price='1000.00',
        )
        DiscountRule.objects.create(
            pk=1,
            enabled=True,
            two_days_discount=20,
            one_day_discount=30,
            expiry_day_discount=50,
        )
        self.client.force_authenticate(user=self.customer)

        response = self.client.post(
            '/api/orders/',
            {'items': [{'product_id': product.pk, 'quantity': 2}]},
            format='json',
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['total'], '1400.00')
        self.assertEqual(response.data['items'][0]['unit_price'], '700.00')
        self.assertEqual(response.data['items'][0]['discount_percent'], 30)
        product.refresh_from_db()
        self.assertEqual(product.quantity, 1)

    def test_order_rejects_expired_or_excess_quantity_without_changing_stock(self):
        expired = Product.objects.create(
            name='Expired Milk',
            expiry_date=self.today - timedelta(days=1),
            quantity=4,
        )
        available = Product.objects.create(
            name='Fresh Milk',
            expiry_date=self.today + timedelta(days=5),
            quantity=2,
        )
        self.client.force_authenticate(user=self.customer)

        expired_response = self.client.post(
            '/api/orders/',
            {'items': [{'product_id': expired.pk, 'quantity': 1}]},
            format='json',
        )
        excess_response = self.client.post(
            '/api/orders/',
            {'items': [{'product_id': available.pk, 'quantity': 3}]},
            format='json',
        )

        self.assertEqual(expired_response.status_code, 400)
        self.assertEqual(excess_response.status_code, 400)
        expired.refresh_from_db()
        available.refresh_from_db()
        self.assertEqual(expired.quantity, 4)
        self.assertEqual(available.quantity, 2)
        self.assertEqual(Order.objects.count(), 0)

    def test_customer_can_only_view_their_own_orders(self):
        order = Order.objects.create(customer=self.customer, total='0.00')
        another_order = Order.objects.create(customer=self.admin, total='0.00')
        self.client.force_authenticate(user=self.customer)
        list_response = self.client.get('/api/orders/')
        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(
            [item['id'] for item in list_response.data],
            [order.pk],
        )
        self.assertEqual(
            self.client.get(f'/api/orders/{order.pk}/').status_code,
            200,
        )

        self.client.force_authenticate(user=self.admin)
        self.assertEqual(
            self.client.get(f'/api/orders/{order.pk}/').status_code,
            404,
        )
        self.assertEqual(
            self.client.get(f'/api/orders/{another_order.pk}/').status_code,
            200,
        )

    def test_reject_zero_or_negative_quantity(self):
        self.client.force_authenticate(user=self.admin)
        res_zero = self.client.post(
            '/api/products/',
            {'name': 'Invalid Zero', 'quantity': 0},
            format='json',
        )
        self.assertEqual(res_zero.status_code, 400)

        res_neg = self.client.post(
            '/api/products/',
            {'name': 'Invalid Negative', 'quantity': -3},
            format='json',
        )
        self.assertEqual(res_neg.status_code, 400)

    def test_null_expiry_dates_sorted_last(self):
        Product.objects.create(name='Salt', expiry_date=None, quantity=2)
        Product.objects.create(
            name='Bread',
            expiry_date=self.today + timedelta(days=1),
            quantity=4,
        )

        res = self.client.get('/api/products/')
        self.assertEqual(res.status_code, 200)
        names = [item['name'] for item in res.data]
        self.assertEqual(names, ['Bread', 'Salt'])

    def test_expiring_endpoint_includes_expired_and_within_3_days(self):
        Product.objects.create(
            name='Expired Yogurt',
            expiry_date=self.today - timedelta(days=1),
            quantity=1,
        )
        Product.objects.create(
            name='Expiring Milk',
            expiry_date=self.today + timedelta(days=2),
            quantity=5,
        )
        Product.objects.create(
            name='Fresh Apples',
            expiry_date=self.today + timedelta(days=10),
            quantity=8,
        )
        Product.objects.create(
            name='Non-perishable Salt',
            expiry_date=None,
            quantity=10,
        )

        res = self.client.get('/api/products/expiring/')
        self.assertEqual(res.status_code, 200)
        names = [item['name'] for item in res.data]
        self.assertEqual(names, ['Expired Yogurt', 'Expiring Milk'])

    def test_only_admin_can_change_discount_rules(self):
        self.client.force_authenticate(user=self.customer)
        customer_response = self.client.patch(
            '/api/discount-rules/',
            {'enabled': False},
            format='json',
        )
        self.assertEqual(customer_response.status_code, 403)

        self.client.force_authenticate(user=self.admin)
        admin_response = self.client.patch(
            '/api/discount-rules/',
            {'enabled': False},
            format='json',
        )
        self.assertEqual(admin_response.status_code, 200)
