from decimal import Decimal, ROUND_HALF_UP

from django.utils import timezone

from .models import DiscountRule


CENT = Decimal('0.01')
_UNSET = object()


def discount_percent_for(product, rules=_UNSET, today=None):
    if rules is _UNSET:
        rules, _ = DiscountRule.objects.get_or_create(pk=1)
    today = today or timezone.localdate()

    if not rules or not rules.enabled or not product.expiry_date:
        return 0

    days_remaining = (product.expiry_date - today).days
    if days_remaining < 0:
        return 0
    if days_remaining == 0:
        return rules.expiry_day_discount
    if days_remaining == 1:
        return rules.one_day_discount
    if days_remaining == 2:
        return rules.two_days_discount
    return 0


def discounted_unit_price(product, discount_percent):
    multiplier = Decimal(100 - discount_percent) / Decimal(100)
    return (product.regular_price * multiplier).quantize(
        CENT,
        rounding=ROUND_HALF_UP,
    )
