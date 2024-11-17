from django.urls import path
from account.views import UserRegistration, UserLogin, UserProfile
urlpatterns = [
    path('user/register/', UserRegistration.as_view(), name='register'),
    path('user/login/', UserLogin.as_view(), name='login'),
    path('user/profile/', UserProfile.as_view(), name='profile'),

    
    
]
