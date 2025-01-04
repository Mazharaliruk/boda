import json
from channels.generic.websocket import AsyncWebsocketConsumer

class CategoryConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "category_updates"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # Receive broadcasted messages
    async def send_category_update(self, event):
        await self.send(text_data=json.dumps(event["content"]))
