import json
from channels.generic.websocket import AsyncWebsocketConsumer
from inventry.serializer import CategorySerializer
from .models import Category

class CategoryConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join the 'categories' group
        self.group_name = "categories"
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the 'categories' group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Handle incoming messages (optional, you can add logic here)
        pass

    # Receive message from the 'categories' group
    async def categories(self, event):
        action = event['content']['action']
        category_data = event['content']['data']

        if action == "create":
            await self.send_category_update(action, category_data)
        elif action == "update":
            await self.send_category_update(action, category_data)
        elif action == "delete":
            await self.send_category_update(action, category_data)

    async def send_category_update(self, action, category_data):
        # Send the category data to the WebSocket
        await self.send(text_data=json.dumps({
            'action': action,
            'category': category_data
        }))
