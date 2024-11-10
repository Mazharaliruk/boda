from django.urls import path, include
from rest_framework import routers
from sales.views import OrderViewSet, TransactionViewSet, PaymentViewSet, PaymentGetwayViewSet

router = routers.DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'paymentgetways', PaymentGetwayViewSet, basename='paymentgetway')

urlpatterns = [
    path('', include(router.urls)),
]
