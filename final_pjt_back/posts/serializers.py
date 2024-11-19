from rest_framework import serializers
from .models import Category, Post, PostLike, Commnet
from accounts.serializers import UserSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_name']


class PostSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'username', 'category', 'expenses_date', 'content', 'image', 'price', 'privacy_setting', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class PostLikeSerializer(serializers.ModelSerializer):
    post = PostSerializer(read_only=True)
    uesr = UserSerializer(read_only=True)

    class Meta:
        model = PostLike
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    post = PostSerializer(read_only=True)

    class Meta:
        model = Commnet
        fields = '__all__'