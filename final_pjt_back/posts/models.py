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
    image = models.ImageField(upload_to='images/', null=True)
    price = models.IntegerField()
    privacy_setting = models.CharField(max_length=20, choices=PRIVACY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')        # 댓글 작성자
    expenses_date = models.DateField()
    content = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author_user_pk = models.IntegerField()