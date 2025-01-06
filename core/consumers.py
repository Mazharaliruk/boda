# chat/consumers.py
import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("Connected to WebSocket...")
        # Get user from scope (provided by AuthMiddlewareStack)
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            await self.close()

        # Create a user-specific group
        self.user_group_name = f"user_{self.user.id}"
        print(self.user_group_name)

        # Join the user's WebSocket group
        await self.channel_layer.group_add(
            self.user_group_name,
            self.channel_name,
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the user's WebSocket group
        await self.channel_layer.group_discard(
            self.user_group_name,
            self.channel_name,
        )

    async def receive(self, text_data):
        # Handle incoming messages (optional, you can add logic here)
        print("Received message:", text_data)

        pass

    # Receive message from the 'messages' group
    async def messages(self, event):
        action = event["content"]["action"]
        message_data = event["content"]["data"]
        print("Received message... action:", action, "message:", message_data)

        if action == "create":
            await self.send_message_update(action, message_data)
        elif action == "update":
            await self.send_message_update(action, message_data)
        elif action == "delete":
            await self.send_message_update(action, message_data)

    async def send_message_update(self, action, message_data):
        # Send the message data to the WebSocket
        await self.send(
            text_data=json.dumps({"action": action, "message": message_data})
        )


# rooms/consumers.py
class RoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join the 'rooms' group
        self.group_name = "chatroom"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        # Accept the WebSocket connection
        await self.accept()
        

    async def disconnect(self, close_code):
        # Leave the 'rooms' group
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        # Handle incoming messages (optional, you can add logic here)

        pass

    # Receive message from the 'rooms' group
    async def chatroom(self, event):
        action = event["content"]["action"]
        room_data = event["content"]["data"]
        print("Received chatroom... action:", action, "chatroom:", room_data)

        if action == "create":
            await self.send_room_update(action, room_data)
        elif action == "update":
            await self.send_room_update(action, room_data)
        elif action == "delete":
            await self.send_room_update(action, room_data)

    async def send_room_update(self, action, room_data):
        # Send the room data to the WebSocket
        await self.send(text_data=json.dumps({"action": action, "chatroom": room_data}))
        