from django.contrib import admin
from inventry.models import Category, SubCategory, Promotion, Discount, Tax


class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'description', 'image_url', 'is_acgtive', 'slug', 'created_at', 'updated_at'
    ]
    search_fields = ['name', 'slug']
    list_filter = ['is_acgtive', 'created_at']
    
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'description', 'image_url', 'is_active', 'slug', 'created_at', 'updated_at', 'category'
    ]
    search_fields = ['name', 'slug']
    list_filter = ['is_active', 'created_at']
    

class PromotionAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'description', 'image_url', 'is_active','created_at', 'updated_at'
    ]
    search_fields = ['name']
    list_filter = ['is_active', 'created_at']
    
    
class DiscountAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'description', 'image_url', 'is_active','created_at', 'updated_at'
    ]
    search_fields = ['name']
    list_filter = ['is_active', 'created_at']


class TaxAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name',  'is_active','created_at', 'updated_at', 'tax_percent', 'start_date', 'end_date', 
        'service_id'
    ]
    
    search_fields = ['name']
    list_filter = ['is_active', 'created_at']
    
# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Promotion, PromotionAdmin)
admin.site.register(Discount, DiscountAdmin)
admin.site.register(Tax, TaxAdmin)


