from django.shortcuts import render
from rest_framework import viewsets
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
    Messages
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
    MessagesSerializer
)


# Create your views here.






class BusinessTypeViewSet(viewsets.ModelViewSet):
    queryset = BusinessType.objects.all()
    serializer_class = BusinessTypeSerializer
    permission_classes = [IsAuthenticated, IsAdmin]  # Only admins can perform any actions

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
        if user.role == 'vendor':
            return self.queryset.filter(user=user)  # Vendors can only access their services
        elif user.role == 'customer':
            return self.queryset.filter(is_active=True)  # Customers see only active services
        return self.queryset  # Admins see everything

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsVendor() | IsAdmin()]  # Vendors and Admins can modify
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
    
    
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    
    
class AIRecommendationViewSet(viewsets.ModelViewSet):
    queryset = AIRecommendation.objects.all()
    serializer_class = AIRecommendationSerializer
    
    
class ChatRoomViewSet(viewsets.ModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    
class MessagesViewSet(viewsets.ModelViewSet):
    queryset = Messages.objects.all()
    serializer_class = MessagesSerializer