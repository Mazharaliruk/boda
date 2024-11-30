from rest_framework import serializers
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


class BusinessTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessType
        fields = '__all__'
        

class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = '__all__'
        
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        
        
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'
        

class EventServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventService
        fields = '__all__'
        
        
class EventMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventMedia
        fields = '__all__'
        
        
class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = '__all__'
        
        
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
        
        
class AIRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIRecommendation
        fields = '__all__'
        
        
class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = '__all__'
        
class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = '__all__'