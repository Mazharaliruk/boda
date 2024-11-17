from django.db import models
from sales.models import Currency

# Create your models here.
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
    vendor = models.ForeignKey('account.VendorProfile', on_delete=models.CASCADE)
    location = models.CharField(blank=True, null=True, max_length=600)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    price = models.FloatField(null=True)
    currency = models.CharField(max_length=3, choices=Currency.choices, default=Currency.PKR),
    image_url = models.URLField(null=True)
    maximum_capacity = models.IntegerField(null=True)
    minimum_capacity = models.IntegerField(null=True)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    
  
  
    
    def __str__(self):
        return self.name