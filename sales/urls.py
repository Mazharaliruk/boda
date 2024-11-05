from django.urls import path
from .views import orders


# URLS
urlpatterns = [
    path('orders/', orders, name='orders')
]
