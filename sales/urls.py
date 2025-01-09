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
    path('by-event/', OrderViewSet.as_view({'get': 'get_orders_by_event'}), name='orders-by-event'),
    path('by-event-status/', OrderViewSet.as_view({'get': 'get_orders_by_event_status'}), name='orders-by-event-status'),
    path('by-vendor/', OrderViewSet.as_view({'get': 'get_orders_by_vendor'}), name='orders-by-vendor'),
    path('by-vendor-status/', OrderViewSet.as_view({'get': 'get_orders_by_vendor_status'}), name='orders-by-vendor-status'),
    path('by-order/', TransactionViewSet.as_view({'get': 'get_transactions_by_order'}), name='transactions-by-order'),
]
