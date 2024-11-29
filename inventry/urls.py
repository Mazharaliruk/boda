from django.urls import path, include
from rest_framework import routers
from inventry.views import CategoryViewSet, SubCategoryViewSet, PromotionViewSet, DiscountViewSet, TaxViewSet

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'subcategories', SubCategoryViewSet, basename='subcategory'),
router.register(r'promotions', PromotionViewSet, basename='promotion'),
router.register(r'discounts', DiscountViewSet, basename='discount'),
router.register(r'taxes', TaxViewSet, basename='tax'),

urlpatterns = [
    path('', include(router.urls)),
]
