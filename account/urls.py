from django.urls import path
from account.views import UserRegistration, UserLogin, UserProfile, UserLogout, UserList, VendorList, CustomerById
urlpatterns = [
    path('user/register/', UserRegistration.as_view(), name='register'),
    path('user/login/', UserLogin.as_view(), name='login'),
    path('user/profile/', UserProfile.as_view(), name='profile'),
    path('user/logout/', UserLogout.as_view(), name='logout'),
    path('user/list/', UserList.as_view(), name='user-list'),
    path('vendor/list/', VendorList.as_view(), name='vendor-list'),
    path('user/<int:pk>/', CustomerById.as_view(), name='customer-by-id'),

    
    
]
