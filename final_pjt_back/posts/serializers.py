from rest_framework import serializers
from .models import Category, Post, PostLike, Commnet


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_name']