# accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.CharField(max_length=20, unique=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    nickname = models.CharField(max_length=30, unique=True)
    birth_date = models.DateField(null=True, blank=True)
    income = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assets = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    point = models.IntegerField(default=0)