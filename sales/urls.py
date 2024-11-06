from django.urls import path
from .views import orders

#GET /api/order_list/?status=COMPLETED&currency=INR&min_amount=100&max_amount=200&min_discount=10&max_discount=20
# 
# URLS
urlpatterns = [
    path('orders/', orders, name='orders')
]
