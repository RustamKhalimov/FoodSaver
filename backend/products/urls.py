from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    DiscountRuleView,
    OrderCollectionView,
    OrderDetailView,
    ProductViewSet,
)


router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
    path('discount-rules/', DiscountRuleView.as_view(), name='discount-rules'),
    path('orders/', OrderCollectionView.as_view(), name='orders'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
]