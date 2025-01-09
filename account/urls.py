from django.urls import path
from account.views import (UserDelete, 
                           UserRegistration,
                           UserLogin, 
                           UserProfile, 
                           UserLogout,
                           UserList, 
                           VendorList, 
                           CustomerById, 
                           CustomerByUser)
urlpatterns = [
    path('user/register/', UserRegistration.as_view(), name='register'),
    path('user/login/', UserLogin.as_view(), name='login'),
    path('user/profile/', UserProfile.as_view(), name='profile'),
    path('user/logout/', UserLogout.as_view(), name='logout'),
    path('user/list/', UserList.as_view(), name='user-list'),
    path('vendor/list/', VendorList.as_view(), name='vendor-list'),
    path('customer/<int:pk>/', CustomerById.as_view(), name='customer-by-id'),
    path('customer_by_user/<str:user>/', CustomerByUser.as_view(), name='customer-by-user'),
    path('user/delete/<int:pk>/', UserDelete.as_view(), name='user-delete'),

]
