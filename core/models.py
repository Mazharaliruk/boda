from django.db import models
from sales.models import Currency

# Create your models here.


#creating choices 
class Status(models.TextChoices):
    DRAFT = 'Draft'
    CONFIRMED = 'Confirmed'
    COMPLETED = 'Completed'
    CANCELLED = 'Cancelled'
    def __str__(self):
        return self.value


class BusinessType(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(null=True)
    image_url = models.URLField(null=True)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(null=True)
    icon_url = models.URLField(null=True)
    

    def __str__(self):
        return self.name
    
    
class Business(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(null=True)
    image_url = models.URLField(null=True)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(null=True)
    business_type = models.ForeignKey(BusinessType, on_delete=models.CASCADE)
    icon_url = models.URLField(null=True)
    
    def __str__(self):
        return self.name
    
    
class Event(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(null=True)
    user = models.ForeignKey('account.CustomerProfile', on_delete=models.CASCADE)# where role is customer
    location = models.CharField(blank=True, null=True, max_length=600)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    price = models.FloatField(null=True)
    currency = models.CharField(max_length=3, choices=Currency.choices, default=Currency.PKR),
    image_url = models.URLField(null=True)
    guest_count = models.IntegerField(null=True)
    budget = models.FloatField(null=True)
    status = models.CharField(max_length=50,choices= Status.choices, default=Status.DRAFT)
    maximum_capacity = models.IntegerField(null=True)
    minimum_capacity = models.IntegerField(null=True)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    
    
    
class Service(models.Model):
        name = models.CharField(max_length=100)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)
        user = models.ForeignKey('account.VendorProfile', on_delete=models.CASCADE) # where role is vendor
        category = models.ForeignKey('inventry.Category', on_delete=models.CASCADE)
        business = models.ForeignKey(Business, on_delete=models.CASCADE)
        description = models.TextField(null=True)
        is_active = models.BooleanField(default=True)
        price = models.FloatField(null=True)
        currency = models.CharField(max_length=3, choices=Currency.choices, default=Currency.PKR)
        
        
        def __str__(self):
            return self.name
        
        
class EventServiceStatus(models.TextChoices):
    PENDING = 'Pending'
    CONFIRMED = 'Confirmed'
    CANCELLED = 'Cancelled'
    def __str__(self):
        return self.value
    
class EventService(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    vendor = models.ForeignKey('account.VendorProfile', on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True)
    price = models.FloatField(null=True)
    currency = models.CharField(max_length=3, choices=Currency.choices, default=Currency.PKR)
    status = models.CharField(max_length=50,choices= EventServiceStatus.choices, default=EventServiceStatus.PENDING)
    
    def __str__(self):
        return self.status
    
    

class MediaType(models.TextChoices):
    IMAGE = 'Image'
    VIDEO = 'Video'
    def __str__(self):
        return self.value
    
class EventMedia(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    media_url = models.URLField(null=True)
    media_type = models.CharField(max_length=50,choices= MediaType.choices, default=MediaType.IMAGE)
    uploaded_at = models.DateTimeField(null=True)
    
    def __str__(self):
        return self.media_url
    
    
    
    
class Reviews(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('account.User', on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    rating = models.IntegerField(null=True)
    comment = models.TextField(null=True)
    
    def __str__(self):
        return self.rating
    

# Notification Table

class Notification(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100)
    message = models.TextField(null=True)
    is_read = models.BooleanField(default=False)
    user = models.ForeignKey('account.User', on_delete=models.CASCADE)
    def __str__(self):
        return self.title
    

class AIRecommendation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('account.User', on_delete=models.CASCADE)
    recommendation_data = models.JSONField(null=True)
    def __str__(self):
        return self.recommendation
    
    
    
    
class RoomStatus(models.TextChoices):
    ACTIVE = 'Active'
    CLOSED = 'Closed'
    ARCHIVED = 'Archived'
    def __str__(self):
        return self.value
    
class RoomType(models.TextChoices):
    CUSTOMER = 'Customer'
    VENDOR = 'Vendor'
    ADMIN = 'Admin'
    def __str__(self):
        return self.value
class ChatRoom(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_id1 = models.ForeignKey('account.VendorProfile', on_delete=models.CASCADE)
    user_id2 = models.ForeignKey('account.CustomerProfile', on_delete=models.CASCADE)
    admin_id = models.ForeignKey('account.AdminProfile', on_delete=models.CASCADE)
    room_status = models.CharField(max_length=50,choices= RoomStatus.choices, default=RoomStatus.ACTIVE)
    room_type = models.CharField(max_length=50,choices= RoomType.choices, default=RoomType.CUSTOMER)
    def __str__(self):
        return self.user_id1
    
    
    
class MessageType(models.TextChoices):
    TEXT = 'Text'
    IMAGE = 'Image'
    VIDEO = 'Video'
    AUDIO = 'Audio',
    FILE = 'File'
    def __str__(self):
        return self.value
class Messages(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    #The ID of the sender (could be customer, vendor, or admin).
    sender_id = models.ForeignKey('account.User', on_delete=models.CASCADE)
    message_content = models.TextField(null=True)
    message_type = models.CharField(max_length=50,choices= MessageType.choices, default=MessageType.TEXT)
    sent_at = models.DateTimeField(null=True)
    read_at = models.DateTimeField(null=True)
    def __str__(self):
        return self.message
        
