from django.urls import path, include
from rest_framework import routers
from core.views import BusinessTypeViewSet

router = routers.DefaultRouter()
router.register(r'businesstypes', BusinessTypeViewSet, basename='businesstype')

urlpatterns = [
    path('', include(router.urls)),
]
