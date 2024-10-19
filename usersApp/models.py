from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models



class User(models.Model):
    full_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    image = models.ImageField(upload_to='menu/', blank=True)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.IntegerField()
    password = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    ordered_at = models.DateTimeField(auto_now_add=True, null=True)



class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    name = models.CharField(max_length=100)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.street}, {self.city} ({self.zip_code})"

