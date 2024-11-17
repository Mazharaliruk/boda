from django.urls import path, include
from rest_framework import routers
from core.views import BusinessTypeViewSet, BusinessViewSet, EventViewSet

router = routers.DefaultRouter()
router.register(r'businesstypes', BusinessTypeViewSet, basename='businesstype'),
router.register(r'businesses', BusinessViewSet, basename='business'),
router.register(r'events', EventViewSet, basename='event')

urlpatterns = [
    path('', include(router.urls)),
]
