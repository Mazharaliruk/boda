# inventry/routing.py
from django.urls import re_path

from core import consumers

cor_url_patterns = [
    re_path('ws/messages/', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/chatroom/(?P<room_id>\d+)/$', consumers.ChatConsumer.as_asgi()),
    re_path('ws/chatrooms/', consumers.RoomConsumer.as_asgi()),
]