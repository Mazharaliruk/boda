from django.shortcuts import render
from rest_framework import viewsets
from core.models import BusinessType,Business, Event
from core.serializer import BusinessTypeSerializer,BusinessSerializer, EventSerializer


# Create your views here.

class BusinessTypeViewSet(viewsets.ModelViewSet):
    queryset = BusinessType.objects.all()
    serializer_class = BusinessTypeSerializer
    

class BusinessViewSet(viewsets.ModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    
    
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
