from django.urls import path, include
from rest_framework import routers
from core.views import (
    BusinessTypeViewSet, 
    BusinessViewSet, 
    EventViewSet, 
    ServiceViewSet, 
    EventServiceViewSet, 
    EventMediaViewSet, 
    ReviewsViewSet, 
    NotificationViewSet, 
    AIRecommendationViewSet,
    ChatRoomViewSet,
    MessagesViewSet
)

router = routers.DefaultRouter()
router.register(r'businesstypes', BusinessTypeViewSet, basename='businesstype'),
router.register(r'businesses', BusinessViewSet, basename='business'),
router.register(r'events', EventViewSet, basename='event'),
router.register(r'services', ServiceViewSet, basename='service'),
router.register(r'eventservices', EventServiceViewSet, basename='eventservice'),
router.register(r'eventmedia', EventMediaViewSet, basename='eventmedia'),
router.register(r'reviews', ReviewsViewSet, basename='review'),
router.register(r'notifications', NotificationViewSet, basename='notification'),
router.register(r'AIRecommendation', AIRecommendationViewSet, basename='AIRecommendation'),
router.register(r'chatroom', ChatRoomViewSet, basename='chatroom'),
router.register(r'messages', MessagesViewSet, basename='messages'),

urlpatterns = [
    path('', include(router.urls)),
]
