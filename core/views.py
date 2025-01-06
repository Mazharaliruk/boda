from time import timezone
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework.permissions import IsAuthenticated
from account.permissions import IsAdmin, IsCustomerOrReadOnly, IsVendor
from core.models import (
    BusinessType,
    Business,
    Event,
    Service,
    EventService,
    EventMedia,
    Reviews,
    Notification,
    AIRecommendation,
    ChatRoom,
    Messages,
)

from core.serializer import (
    BusinessTypeSerializer,
    BusinessSerializer,
    EventSerializer,
    ServiceSerializer,
    EventServiceSerializer,
    EventMediaSerializer,
    ReviewsSerializer,
    NotificationSerializer,
    AIRecommendationSerializer,
    ChatRoomSerializer,
    MessagesSerializer,
)


# Create your views here.


class BusinessTypeViewSet(viewsets.ModelViewSet):
    queryset = BusinessType.objects.all()
    serializer_class = BusinessTypeSerializer
    permission_classes = [
        IsAuthenticated,
        IsAdmin,
    ]  # Only admins can perform any actions


class BusinessViewSet(viewsets.ModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    permission_classes = [IsAuthenticated]  # Restrict access to authenticated users


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == "vendor":
            return self.queryset.filter(
                user=user
            )  # Vendors can only access their services
        elif user.role == "customer":
            return self.queryset.filter(
                is_active=True
            )  # Customers see only active services
        return self.queryset  # Admins see everything

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [
                IsAuthenticated(),
                IsVendor() | IsAdmin(),
            ]  # Vendors and Admins can modify
        return [IsAuthenticated(), IsCustomerOrReadOnly()]  # Customers can only view


class EventServiceViewSet(viewsets.ModelViewSet):
    queryset = EventService.objects.all()
    serializer_class = EventServiceSerializer


class EventMediaViewSet(viewsets.ModelViewSet):
    queryset = EventMedia.objects.all()
    serializer_class = EventMediaSerializer


class ReviewsViewSet(viewsets.ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer

    @action(detail=False, methods=["get"], url_path="by-event")
    def get_reviews_by_event(self, request):
        event = request.query_params.get("event")
        if not event:
            return Response({"error": "event query parameter is required."}, status=400)
        reviews = Reviews.objects.filter(event=event)
        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data)


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


class AIRecommendationViewSet(viewsets.ModelViewSet):
    queryset = AIRecommendation.objects.all()
    serializer_class = AIRecommendationSerializer


class ChatRoomViewSet(viewsets.ModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        chat_room = serializer.save()
        self.broadcast_chatroom_update("create", chat_room)
        

    def perform_update(self, serializer):
        print("Performing update...")
        chat_room = serializer.save()
        self.broadcast_chatroom_update("update", chat_room)

    def perform_destroy(self, instance):
        self.broadcast_chatroom_update("delete", instance)
        instance.delete()

    def broadcast_chatroom_update(self, action, chat_room):
        print("Broadcasting chatroom update... action:", action, "chatroom:", chat_room)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "chatroom",  # This is the group name
            {
                "type": "chatroom",  # This is the method we will call in the consumer
                "content": {
                    "action": action,
                    "data": (
                        ChatRoomSerializer(chat_room).data
                        if action != "delete"
                        else {"id": chat_room.id}
                    ),
                },
            },
        )


class MessagesViewSet(viewsets.ModelViewSet):
    queryset = Messages.objects.all()
    serializer_class = MessagesSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):

        message = serializer.save()
        self.broadcast_message_update("create", message)

    def perform_update(self, serializer):
        print("Performing update...")
        message = serializer.save()
        self.broadcast_message_update("update", message)

    def perform_destroy(self, instance):
        self.broadcast_message_update("delete", instance)
        instance.delete()

    def broadcast_message_update(self, action, message):
        print("Broadcasting message update... action:", action, "message:", message)
        channel_layer = get_channel_layer()
        if not channel_layer:
            print("Channel layer not initialized!")
            return

        serialized_data = (
            MessagesSerializer(message).data
            if action != "delete"
            else {"id": message.id}
        )

        # If the message is part of a room, broadcast to the room group
        if message.room:
            room_group_name = f"room_{message.room.id}"
            print(f"Broadcasting to room group: {room_group_name}")
            async_to_sync(channel_layer.group_send)(
                room_group_name,
                {
                    "type": "messages",
                    "content": {"action": action, "data": serialized_data},
                },
            )
        else:
            # Individual messaging logic
            if message.receiver_id:
                receiver_group_name = f"user_{message.receiver_id.id}"
                print(f"Broadcasting to individual group: {receiver_group_name}")
                async_to_sync(channel_layer.group_send)(
                    receiver_group_name,
                    {
                        "type": "messages",
                        "content": {"action": action, "data": serialized_data},
                    },
                )

