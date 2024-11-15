from django.urls import path
from account.views import UserRegistration
urlpatterns = [
    path('user/register/', UserRegistration.as_view(), name='register'),
    
    
]
