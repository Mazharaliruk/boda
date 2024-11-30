from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.


#Roles
ROLES = (
    ('admin', 'Admin'),
    ('customer', 'Customer'),
    ('vendor', 'Vendor'),
)



class UserManager(BaseUserManager):
    def create_user(self, email, name, phone, date_of_birth, password=None, password2=None, role=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")
          # Ensure 'admin' role cannot be set here
        if role == 'admin':
            raise ValueError("Cannot create a user with role 'admin' using this method.")
        if role is None:
            role = 'customer'
        if role not in ['customer', 'vendor']:
            raise ValueError("Invalid role. Role must be 'customer' or 'vendor'.")
        print(f"Creating user with role: {role}")  # Debug line to log role
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            phone=phone,
            date_of_birth=date_of_birth,
            role=role
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, phone, date_of_birth, password=None):
            """
            Creates and saves a superuser with the given email, date of
            birth and password.
            """
            user = self.create_user(
                email,
                password=password,
                name=name,
                phone=phone,
                date_of_birth=date_of_birth,
            )
            user.role = 'admin'
            user.save(using=self._db)
              # Remove any incorrect profiles
            if hasattr(user, 'customerprofile'):
                user.customerprofile.delete()
              # Explicitly create AdminProfile to avoid signal conflict
            if not hasattr(user, 'adminprofile'):
                AdminProfile.objects.create(user=user)
            return user




class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email",
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    # is_admin = models.BooleanField(default=False)
    role = models.CharField(max_length=20, choices=ROLES, default='customer')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["date_of_birth","name","phone"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return self.role == 'admin'

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.role == 'admin'


# Profile Models
class VendorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='vendor_profiles/', blank=True, null=True)
    business_name = models.CharField(max_length=255)
    business_type = models.ForeignKey('core.BusinessType', on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CustomerProfile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='customer_profiles/', blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)  # Add more fields as needed
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='admin_profiles/', blank=True, null=True)
    permissions = models.TextField(blank=True)  # Add fields as needed
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    # Signals to Create Profile on User Creation
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    print(f"Signal create_user_profile triggered for user: {instance.email}, role: {instance.role}")
    if created:
        # Only create profile for the assigned role
        if instance.role == 'vendor' and not hasattr(instance, 'vendorprofile'):
            VendorProfile.objects.create(user=instance)
        elif instance.role == 'customer' and not hasattr(instance, 'customerprofile'):
            CustomerProfile.objects.create(user=instance)
        elif instance.role == 'admin' and not hasattr(instance, 'adminprofile'):
            AdminProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    print(f"Signal save_user_profile triggered for user: {instance.email}, role: {instance.role}")

    # Save the corresponding profile if it exists
    if instance.role == 'vendor' and hasattr(instance, 'vendorprofile'):
        instance.vendorprofile.save()
    elif instance.role == 'customer' and hasattr(instance, 'customerprofile'):
        instance.customerprofile.save()
    elif instance.role == 'admin' and hasattr(instance, 'adminprofile'):
        instance.adminprofile.save()
