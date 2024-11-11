from django.db import models

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