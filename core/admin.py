from django.contrib import admin
from core.models import (
     BusinessType, 
     Business, 
     Event, 
     Service, 
     EventService, 
     EventMedia, 
     Reviews,
     Notification, 
     AIRecommendation,
     ChatRoom,
     Messages
)

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
    list_display = ('name',  'created_at', 'updated_at','description', 
                    'image_url',  'business', 'user', 'location', 
                    'start_date', 'end_date', 'price', 'currency',
                    'guest_count', 'budget', 'status',
                    'maximum_capacity', 'minimum_capacity')
    search_fields = ['name', 'slug']
    list_filter = ['created_at']
    
    
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description','is_active', 'created_at', 'updated_at','vendor')
    search_fields = ['name',]
    list_filter = ['created_at','is_active']
    

class EventServiceAdmin(admin.ModelAdmin):
    list_display = ('event','service', 'vendor', 'quantity', 'price', 'currency', 'status')
    search_fields = ['event', 'service']
    list_filter = ['created_at', 'status']
    
    
class EventMediaAdmin(admin.ModelAdmin):
    list_display = ('event_service', 'media_file', 'created_at', 'updated_at','media_type')
    search_fields = ['event_service', 'media_type']
    list_filter = ['created_at','media_type']
    
    
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created_at', 'updated_at','is_read')
    search_fields = ['user', 'message']
    list_filter = ['created_at','is_read']
    
    
class ReviewsAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'service', 'user', 'comment', 'created_at', 'updated_at','rating', 'vendor', 'event')
    search_fields = ['service', 'user'] 
    list_filter = ['created_at']
    
class AIRecommendationAdmin(admin.ModelAdmin):
    list_display = ('user', 'recommendation_data', 'created_at', 'updated_at',)
    search_fields = ['user', 'recommendation_data']
    list_filter = ['created_at']
    
    
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('user_id1', 'user_id2', 'created_at', 'updated_at', 'room_status', 'room_type')
    list_filter = ['created_at', 'room_status', 'room_type']
    
    
    
    
class MessagesAdmin(admin.ModelAdmin):
    list_display = ('room', 'sender_id', 'message_content', 'message_type', 'sent_at', 'read_at')
    list_filter = ['message_type',]
    
    

admin.site.register(BusinessType, BusinessTypeAdmin)
admin.site.register(Business, BusinessAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(EventService, EventServiceAdmin)
admin.site.register(EventMedia, EventMediaAdmin)
admin.site.register(Reviews, ReviewsAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(AIRecommendation, AIRecommendationAdmin)
admin.site.register(ChatRoom, ChatRoomAdmin)
admin.site.register(Messages, MessagesAdmin)