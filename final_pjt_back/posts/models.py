from django.db import models
from django.conf import settings


# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=20)


PRIVACY_CHOICES = [
    ('public', 'Public'),
    ('private', 'Private'),
    ('subscriber', 'Subscriber'),
]


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    expenses_date = models.DateField(null=False)
    content = models.TextField(null=False)
    image = models.ImageField(upload_to='images/posts/', null=True)
    price = models.IntegerField()
    privacy_setting = models.CharField(max_length=20, choices=PRIVACY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Commnet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)