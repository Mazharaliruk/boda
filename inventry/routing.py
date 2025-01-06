# inventry/routing.py
from django.urls import re_path

from inventry import consumers

category_url_patterns = [
    re_path('ws/categories/', consumers.CategoryConsumer.as_asgi()),
]