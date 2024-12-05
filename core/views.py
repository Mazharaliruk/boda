from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
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
    permission_classes = [IsAuthenticated]  # Restrict access to authenticated users
    

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