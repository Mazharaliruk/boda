from django.shortcuts import render
from rest_framework import viewsets
from core.models import BusinessType
from core.serializer import BusinessTypeSerializer


# Create your views here.

class BusinessTypeViewSet(viewsets.ModelViewSet):
    queryset = BusinessType.objects.all()
    serializer_class = BusinessTypeSerializer
