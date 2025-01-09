# chat/consumers.py
import json
from asgiref.sync import sync_to_async

from channels.generic.websocket import AsyncWebsocketConsumer

from core.models import ChatRoom


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("Connected to WebSocket...")
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            await self.close()

        # Handle user role and room-specific group joining
        self.room_id = self.scope["url_route"]["kwargs"].get("room_id")  # Extract room_id from the WebSocket URL
        print("Room ID:", self.room_id)
        if self.room_id:
            print("Joining room...")
            self.room_group_name = f"room_{self.room_id}"
            print(f"Joining room group: {self.room_group_name}")

            # Check if user has permission to join this room
            if not await self.user_has_permission():
                await self.close()
                return

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name,
            )
        else:  # Handle user-specific group for direct messages
            self.user_group_name = f"user_{self.user.id}"
            print(f"Joining user group: {self.user_group_name}")
            await self.channel_layer.group_add(
                self.user_group_name,
                self.channel_name,
            )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave appropriate group
        if hasattr(self, "room_group_name"):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name,
            )
        elif hasattr(self, "user_group_name"):
            await self.channel_layer.group_discard(
                self.user_group_name,
                self.channel_name,
            )

    async def user_has_permission(self):
        print("Checking user permission...")
        try:
            room = await sync_to_async(ChatRoom.objects.get)(id=self.room_id)
            user_id1 = await sync_to_async(lambda: room.user_id1.user)()
            user_id2 = await sync_to_async(lambda: room.user_id2.user)()
            admin_id = await sync_to_async(lambda: room.admin_id.user)()

            print(f"user_id1: {user_id1}, user_id2: {user_id2}, admin_id: {admin_id}, current_user: {self.scope['user'].id}")

            return self.scope["user"].id in [user_id1.id, user_id2.id, admin_id.id]
        except ChatRoom.DoesNotExist:
            print("Room does not exist.")
            return False



    async def messages(self, event):
        action = event["content"]["action"]
        message_data = event["content"]["data"]
        print("Received message... action:", action, "message:", message_data)

        if action in ["create", "update", "delete"]:
            await self.send_message_update(action, message_data)

    async def send_message_update(self, action, message_data):
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
        