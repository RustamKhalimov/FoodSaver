from datetime import timedelta, time
from decimal import Decimal

from django.core import mail
from django.core.management import call_command
from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.utils import timezone
from rest_framework.test import APIClient

from products.models import Product
from .models import ReminderDelivery, UserProfile, get_user_role


class AccountAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_registration_creates_customer_and_ignores_submitted_role(self):
        response = self.client.post(
            '/api/accounts/register/',
            {
                'username': 'new-customer',
                'email': 'customer@example.com',
                'password': 'StrongPass123!xyz',
                'role': UserProfile.ROLE_ADMIN,
            },
            format='json',
        )

        self.assertEqual(response.status_code, 201)
        user = User.objects.get(username='new-customer')
        self.assertEqual(user.profile.role, UserProfile.ROLE_CUSTOMER)
        self.assertEqual(response.data['role'], UserProfile.ROLE_CUSTOMER)
        self.assertEqual(response.data['user']['role'], UserProfile.ROLE_CUSTOMER)

    def test_customer_and_admin_login_return_backend_assigned_roles(self):
        customer = User.objects.create_user(
            username='customer',
            email='customer@example.com',
            password='StrongPass123!xyz',
        )
        customer.profile.role = UserProfile.ROLE_CUSTOMER
        customer.profile.save()

        admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='StrongPass123!xyz',
        )
        admin.profile.role = UserProfile.ROLE_ADMIN
        admin.profile.save()

        customer_response = self.client.post(
            '/api/accounts/login/',
            {'email': customer.email, 'password': 'StrongPass123!xyz'},
            format='json',
        )
        admin_response = self.client.post(
            '/api/accounts/login/',
            {'email': admin.email, 'password': 'StrongPass123!xyz'},
            format='json',
        )

        self.assertEqual(customer_response.status_code, 200)
        self.assertEqual(customer_response.data['role'], UserProfile.ROLE_CUSTOMER)
        self.assertEqual(admin_response.status_code, 200)
        self.assertEqual(admin_response.data['role'], UserProfile.ROLE_ADMIN)

    def test_django_superusers_are_admin_even_if_profile_defaulted_to_customer(self):
        admin = User.objects.create_superuser(
            username='django-admin',
            email='django-admin@example.com',
            password='StrongPass123!xyz',
        )

        self.assertEqual(admin.profile.role, UserProfile.ROLE_CUSTOMER)
        self.assertEqual(get_user_role(admin), UserProfile.ROLE_ADMIN)

        self.client.force_authenticate(user=admin)
        response = self.client.get('/api/accounts/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['role'], UserProfile.ROLE_ADMIN)

    def test_profile_saves_and_restores_reminder_preferences(self):
        customer = User.objects.create_user(
            username='reminder-customer',
            email='reminder@example.com',
            password='StrongPass123!xyz',
        )
        self.client.force_authenticate(user=customer)

        initial = self.client.get('/api/accounts/profile/')
        self.assertEqual(initial.status_code, 200)
        self.assertFalse(initial.data['notifications_enabled'])
        self.assertEqual(initial.data['reminder_time'], '09:00')

        updated = self.client.patch(
            '/api/accounts/profile/',
            {'notifications_enabled': True, 'reminder_time': '17:45'},
            format='json',
        )
        self.assertEqual(updated.status_code, 200)
        self.assertTrue(updated.data['notifications_enabled'])
        self.assertEqual(updated.data['reminder_time'], '17:45')

        restored = self.client.get('/api/accounts/profile/')
        self.assertTrue(restored.data['notifications_enabled'])
        self.assertEqual(restored.data['reminder_time'], '17:45')

        disabled = self.client.patch(
            '/api/accounts/profile/',
            {'notifications_enabled': False},
            format='json',
        )
        self.assertEqual(disabled.status_code, 200)
        self.assertFalse(disabled.data['notifications_enabled'])


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class ExpiryReminderCommandTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='email-reminder-customer',
            email='email-reminder@example.com',
            password='StrongPass123!xyz',
        )
        self.user.profile.notifications_enabled = True
        self.user.profile.reminder_time = time(9, 0)
        self.user.profile.save(update_fields=['notifications_enabled', 'reminder_time'])
        Product.objects.create(
            name='Reminder Milk',
            category='Dairy',
            quantity=2,
            regular_price=Decimal('850.00'),
            expiry_date=timezone.localdate() + timedelta(days=1),
        )

    def test_command_sends_one_daily_email_with_expiring_items(self):
        call_command('send_expiry_reminders', at='09:00')

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [self.user.email])
        self.assertIn('Reminder Milk', mail.outbox[0].body)
        self.assertEqual(ReminderDelivery.objects.filter(user=self.user).count(), 1)

        call_command('send_expiry_reminders', at='09:00')
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(ReminderDelivery.objects.filter(user=self.user).count(), 1)

    def test_command_dry_run_does_not_send_or_record(self):
        call_command('send_expiry_reminders', at='09:00', dry_run=True)

        self.assertEqual(mail.outbox, [])
        self.assertFalse(ReminderDelivery.objects.filter(user=self.user).exists())

    def test_command_skips_when_no_products_are_expiring(self):
        Product.objects.all().delete()

        call_command('send_expiry_reminders', at='09:00')

        self.assertEqual(mail.outbox, [])
        self.assertFalse(ReminderDelivery.objects.filter(user=self.user).exists())
