from django.db import models

from inventry.validator import validate_video_file

class Category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(null=True, blank=True)
    service = models.ForeignKey('core.Service', on_delete=models.CASCADE, null= True, blank= True)
    image_url = models.ImageField(upload_to='categories/',null=True, blank=True)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(null=True, blank=True)
    
    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(null=True, blank= True)
    image_url = models.ImageField(upload_to='subcategories/',null=True, blank=True)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(null=True, blank= True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    
class Promotion(models.Model):
    name = models.CharField(max_length=100, null= True, blank= True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    vendor_id = models.ForeignKey('account.VendorProfile', on_delete=models.CASCADE, null=True, blank= True)  # where role is vendor
    description = models.TextField(null=True, blank=True)
    image_url = models.ImageField(upload_to='promotions/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    video_url = models.FileField(
        upload_to='promotions/videos/',
        null=True,
        blank=True,
        validators=[validate_video_file]
    )
    discount_percent = models.FloatField(null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
class Discount(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    vendor_id = models.ForeignKey('account.VendorProfile', on_delete=models.CASCADE, null=True, blank= True) # where role is vendor
    service = models.ForeignKey('core.Service', on_delete=models.CASCADE, null=True, blank= True)
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE, null=True, blank= True)
    description = models.TextField(null=True, blank= True)
    image_url = models.ImageField(upload_to='discount/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    discount_percent= models.FloatField(null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    

    
class Tax(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    service_id = models.ForeignKey('core.Service', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    tax_percent= models.FloatField(null=True, blank= True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    description = models.TextField(null=True, blank= True)
    
    def __str__(self):
        return self.name
