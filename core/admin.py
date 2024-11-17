from django.contrib import admin
from core.models import BusinessType, Business, Event

# Register your models here.
class BusinessTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'image_url', 'is_active', 'slug', 'icon_url')
    search_fields = ['name', 'slug']
    list_filter = ['is_active', 'created_at']
    

class BusinessAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'image_url', 'is_active', 'slug', 'business_type', 'icon_url')
    search_fields = ['name', 'slug']
    list_filter = ['is_active', 'created_at']
    

class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'image_url',  'business')
    search_fields = ['name', 'slug']
    list_filter = ['created_at']
    
    

admin.site.register(BusinessType, BusinessTypeAdmin)
admin.site.register(Business, BusinessAdmin)
admin.site.register(Event, EventAdmin)