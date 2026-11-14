from decimal import Decimal
from datetime import timedelta

from django.db import transaction
from django.db.models import F, Q
from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsAdminUser
from .models import DiscountRule, Order, OrderItem, Product
from .pricing import discount_percent_for, discounted_unit_price
from .serializers import (
    DiscountRuleSerializer,
    OrderCreateSerializer,
    OrderSerializer,
    ProductSerializer,
)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by(
        F('expiry_date').asc(nulls_last=True),
        'name'
    )
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in {'create', 'update', 'partial_update', 'destroy'}:
            return [IsAdminUser()]
        return [permissions.AllowAny()]

    @action(detail=False, methods=['get'])
    def expiring(self, request):
        today = timezone.localdate()
        last_day = today + timedelta(days=3)

        products = Product.objects.filter(
            expiry_date__isnull=False,
            expiry_date__lte=last_day
        ).order_by('expiry_date', 'name')

        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def catalog(self, request):
        today = timezone.localdate()
        products = Product.objects.filter(quantity__gt=0).filter(
            Q(expiry_date__isnull=True) | Q(expiry_date__gte=today)
        ).order_by(
            F('expiry_date').asc(nulls_last=True),
            'name',
        )
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)


@transaction.atomic
def create_order_for_customer(customer, items):
    today = timezone.localdate()
    rules, _ = DiscountRule.objects.get_or_create(pk=1)
    products = {}

    for item in sorted(items, key=lambda line: line['product_id']):
        try:
            product = Product.objects.select_for_update().get(
                pk=item['product_id']
            )
        except Product.DoesNotExist:
            raise ValidationError({
                'items': f"Product {item['product_id']} is no longer available."
            })

        quantity = item['quantity']
        if product.quantity < quantity:
            raise ValidationError({
                'items': f'Only {product.quantity} of {product.name} are available.'
            })
        if product.expiry_date and product.expiry_date < today:
            raise ValidationError({
                'items': f'{product.name} has expired and cannot be ordered.'
            })
        products[product.pk] = (product, quantity)

    prepared_items = []
    total = Decimal('0.00')
    for product, quantity in products.values():
        discount = discount_percent_for(product, rules=rules, today=today)
        unit_price = discounted_unit_price(product, discount)
        line_total = unit_price * quantity
        total += line_total
        prepared_items.append({
            'product': product,
            'product_name': product.name,
            'quantity': quantity,
            'original_unit_price': product.regular_price,
            'unit_price': unit_price,
            'discount_percent': discount,
            'line_total': line_total,
        })

    for product, quantity in products.values():
        updated = Product.objects.filter(
            pk=product.pk,
            quantity__gte=quantity,
        ).update(quantity=F('quantity') - quantity)
        if updated != 1:
            raise ValidationError({
                'items': f'{product.name} stock changed. Please review your cart.'
            })

    order = Order.objects.create(customer=customer, total=total)
    OrderItem.objects.bulk_create([
        OrderItem(order=order, **item) for item in prepared_items
    ])
    return order


class OrderCollectionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(customer=request.user).prefetch_related('items')
        return Response(OrderSerializer(orders, many=True).data)

    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = create_order_for_customer(
            request.user,
            serializer.validated_data['items'],
        )
        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED,
        )


class OrderDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            order = Order.objects.prefetch_related('items').get(
                pk=pk,
                customer=request.user,
            )
        except Order.DoesNotExist:
            raise NotFound('Order not found.')
        return Response(OrderSerializer(order).data)


class DiscountRuleView(APIView):
    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [IsAdminUser()]

    def get(self, request):
        rules, created = DiscountRule.objects.get_or_create(pk=1)

        serializer = DiscountRuleSerializer(rules)
        return Response(serializer.data)

    def patch(self, request):
        rules, created = DiscountRule.objects.get_or_create(pk=1)

        serializer = DiscountRuleSerializer(
            rules,
            data=request.data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def put(self, request):
        rules, created = DiscountRule.objects.get_or_create(pk=1)

        serializer = DiscountRuleSerializer(
            rules,
            data=request.data
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
