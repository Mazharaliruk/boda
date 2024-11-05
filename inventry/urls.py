from django.urls import path
from .views import category_list


# URLS
urlpatterns = [
    path('category_list/', category_list, name='category_list')
]
