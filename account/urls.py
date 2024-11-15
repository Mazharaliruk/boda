from django.urls import path
from account.views import UserRegistration, UserLogin
urlpatterns = [
    path('user/register/', UserRegistration.as_view(), name='register'),
    path('user/login/', UserLogin.as_view(), name='login'),
    
    
]
