from rest_framework import serializers
from .models import DiscountRule, Order, OrderItem, Product
from .pricing import discount_percent_for, discounted_unit_price


class ProductSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(min_value=1)
    discount_percent = serializers.SerializerMethodField()
    discounted_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'barcode',
            'image_url',
            'category',
            'quantity',
            'regular_price',
            'unit_size',
            'expiry_date',
            'created_at',
            'updated_at',
            'discount_percent',
            'discounted_price',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'discount_percent', 'discounted_price']

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError('Quantity must be at least 1.')
        return value

    def get_discount_percent(self, product):
        if 'discount_rules' not in self.context:
            rules, _ = DiscountRule.objects.get_or_create(pk=1)
            self.context['discount_rules'] = rules
        return discount_percent_for(
            product,
            rules=self.context['discount_rules'],
        )

    def get_discounted_price(self, product):
        discount = self.get_discount_percent(product)
        return discounted_unit_price(product, discount)


class DiscountRuleSerializer(serializers.ModelSerializer):
    two_days_discount = serializers.IntegerField(min_value=0, max_value=100)
    one_day_discount = serializers.IntegerField(min_value=0, max_value=100)
    expiry_day_discount = serializers.IntegerField(min_value=0, max_value=100)

    class Meta:
        model = DiscountRule
        fields = [
            'id',
            'enabled',
            'two_days_discount',
            'one_day_discount',
            'expiry_day_discount',
            'updated_at',
        ]
        read_only_fields = ['id', 'updated_at']


class OrderLineInputSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(min_value=1)
    quantity = serializers.IntegerField(min_value=1)


class OrderCreateSerializer(serializers.Serializer):
    items = OrderLineInputSerializer(many=True, allow_empty=False)

    def validate_items(self, items):
        if len(items) > 50:
            raise serializers.ValidationError('An order can contain at most 50 products.')

        product_ids = [item['product_id'] for item in items]
        if len(product_ids) != len(set(product_ids)):
            raise serializers.ValidationError('Each product must appear only once.')
        return items


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            'id',
            'product',
            'product_name',
            'quantity',
            'original_unit_price',
            'unit_price',
            'discount_percent',
            'line_total',
        ]
        read_only_fields = fields


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'status', 'total', 'created_at', 'items']
        read_only_fields = fields