from django.contrib import admin
from account.models import User, VendorProfile, CustomerProfile, AdminProfile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
 

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["id","email", "name" ,"date_of_birth", "phone","is_active", "role","created_at","updated_at"]
    list_filter = ["role"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["name","phone","date_of_birth"]}),
        ("Permissions", {"fields": ["role"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "name", "date_of_birth", "phone", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email", "id"]
    ordering = ["email","id"]
    filter_horizontal = []


# Customer Profile  Admin
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ["id","user_id", "user", "created_at", "updated_at"]
    search_fields = ["user__email", "user__id"]
    ordering = ["user__email", "user__id"]
    filter_horizontal = [
        
    ]
    
    
class VendorProfileAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "created_at", "updated_at"]
    search_fields = ["user__email", "user__id"]
    ordering = ["user__email", "user__id"]
    filter_horizontal = [
        
    ]
    
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "created_at", "updated_at"]
    search_fields = ["user__email", "id"]
    ordering = ["user__email", "user__id"]
    filter_horizontal = [
        
    ]

# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
admin.site.register(CustomerProfile, CustomerProfileAdmin),
admin.site.register(VendorProfile, VendorProfileAdmin),
admin.site.register(AdminProfile, AdminProfileAdmin),
