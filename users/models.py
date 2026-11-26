from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.db import models


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(email, password, **extra_fields)



class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True
    )

    phone_number = models.CharField(
        max_length=15,
        blank=True,
        default=''
    )


class Address(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='addresses'
    )
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    house_name = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.city}"    


class OTPVerification(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='otp_verifications'
    )
    otp_hash = models.CharField(max_length=255)
    purpose = models.CharField(max_length=30)
    attempts = models.PositiveIntegerField(default=0)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.purpose}"    