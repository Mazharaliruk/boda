from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(null=True)
    image_url = models.URLField(null=True)
    is_acgtive = models.BooleanField(default=True)
    slug = models.SlugField(null=True)
    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(null=True)
    image_url = models.URLField(null=True)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    
class Promotion(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    vendor_id = models.ForeignKey('account.VendorProfile', on_delete=models.CASCADE) # where role is vendor
    description = models.TextField(null=True)
    image_url = models.URLField(null=True)
    is_active = models.BooleanField(default=True)
    discount_percent= models.FloatField(null=True)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    
    
    def __str__(self):
        return self.name
    
class Discount(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    vendor_id = models.ForeignKey('account.VendorProfile', on_delete=models.CASCADE) # where role is vendor
    service = models.ForeignKey('core.Service', on_delete=models.CASCADE)
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE)
    description = models.TextField(null=True)
    image_url = models.URLField(null=True)
    is_active = models.BooleanField(default=True)
    discount_percent= models.FloatField(null=True)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    
    def __str__(self):
        return self.name
    
    
class Tax(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    service_id = models.ForeignKey('core.Service', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    tax_percent= models.FloatField(null=True)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    
    def __str__(self):
        return self.name
