from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from inventry.models import Category, SubCategory, Promotion, Discount, Tax
from inventry.serializer import CategorySerializer, SubCategorySerializer, PromotionSerializer, DiscountSerializer, TaxSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        print("Performing create...")
        category = serializer.save()
        self.broadcast_category_update("create", category)

    def perform_update(self, serializer):
        print("Performing update...")
        category = serializer.save()
        self.broadcast_category_update("update", category)

    def perform_destroy(self, instance):
        self.broadcast_category_update("delete", instance)
        instance.delete()

    def broadcast_category_update(self, action, category):
        print("Broadcasting category update... action:", action, "category:", category)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "categories",  # This is the group name
            {
                "type": "categories",  # This is the method we will call in the consumer
                "content": {
                    "action": action,
                    "data": CategorySerializer(category).data if action != "delete" else {"id": category.id},
                },
            },
        )


class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = [IsAuthenticated]  # Restrict access to authenticated users
    
    
class PromotionViewSet(viewsets.ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    permission_classes = [IsAuthenticated]  # Restrict access to authenticated users
    
    
class DiscountViewSet(viewsets.ModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = [IsAuthenticated]  # Restrict access to authenticated users
    
    
class TaxViewSet(viewsets.ModelViewSet):
    queryset = Tax.objects.all()
    serializer_class = TaxSerializer
    permission_classes = [IsAuthenticated]  # Restrict access to authenticated users