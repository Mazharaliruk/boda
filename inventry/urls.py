from django.urls import path, include
from rest_framework import routers
from inventry.views import CategoryViewSet

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
]
