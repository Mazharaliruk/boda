from django.contrib import admin
from inventry.models import Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'description', 'image_url', 'is_acgtive', 'slug', 'created_at', 'updated_at'
    ]
    search_fields = ['name', 'slug']
    list_filter = ['is_acgtive', 'created_at']

# Register your models here.
admin.site.register(Category, CategoryAdmin)


