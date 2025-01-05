# inventry/routing.py
from django.urls import re_path

from inventry import consumers

websocket_urlpatterns = [
    re_path('ws/categories/', consumers.CategoryConsumer.as_asgi()),
]