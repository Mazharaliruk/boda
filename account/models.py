from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Create your models here.


#Roles
ROLES = (
    ('admin', 'Admin'),
    ('customer', 'Customer'),
    ('vendor', 'Vendor'),
)



class UserManager(BaseUserManager):
    def create_user(self, email, name, phone, date_of_birth, password=None, password2=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            phone=phone,
            date_of_birth=date_of_birth,
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
