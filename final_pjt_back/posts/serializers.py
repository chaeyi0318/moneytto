from rest_framework import serializers
from .models import Category, Post, PostLike, Comment
from accounts.models import Budget
from accounts.serializers import UserSerializer
from datetime import datetime


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_name']


class PostSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    # user_pk = serializers.IntegerField(source='user.id', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'username', 'category', 'expenses_date', 'content', 'image', 'price', 'privacy_setting', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("가격은 음수일 수 없습니다.")
        return value


class PostLikeSerializer(serializers.ModelSerializer):
    post = PostSerializer(read_only=True)
    uesr = UserSerializer(read_only=True)

    class Meta:
        model = PostLike
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    created_at_formatted = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'author_user_pk', 'user', 'expenses_date', 'content', 'created_at_formatted', 'updated_at']

    def get_created_at_formatted(self, obj):
        # created_at을 원하는 형식으로 변환
        return obj.created_at.strftime("%Y-%m-%d %H:%M:%S")


class CalendarMainSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    username = serializers.CharField(source='user.username', read_only=True)
    owner = serializers.IntegerField(source='user.pk', read_only=True)
    amount = serializers.SerializerMethodField()        # 예산
    
    class Meta:
        model = Post
        fields = ['id', 'username', 'owner', 'expenses_date', 'image', 'amount']

    def get_image(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            return obj.image.url
        return None
    
    def get_amount(self, obj):
        year = obj.expenses_date.year
        month = obj.expenses_date.month
        budget = Budget.objects.filter(user=obj.user, year=year, month=month).first()
        return budget.amount if budget else 0  # 예산이 없으면 0 반환
    
# class CalendarMainExpenseSerializer(serializers.ModelSerializer):
#     image = serializers.SerializerMethodField()
#     username = serializers.CharField(source='user.username', read_only=True)
#     owner = serializers.IntegerField(source='user.pk', read_only=True)
#     amount = serializers.SerializerMethodField()        # 예산
    
#     class Meta:
#         model = Post
#         fields = ['id', 'username', 'owner', 'expenses_date', 'image', 'amount', 'price']

#     def get_image(self, obj):
#         if obj.image and hasattr(obj.image, 'url'):
#             return obj.image.url
#         return None
    
#     def get_amount(self, obj):
#         year = obj.expenses_date.year
#         month = obj.expenses_date.month
#         budget = Budget.objects.filter(user=obj.user, year=year, month=month).first()
#         return budget.amount if budget else 0  # 예산이 없으면 0 반환
    

class PostDetailSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    category_name = serializers.ReadOnlyField(source='category.category_name')
    username = serializers.CharField(source='user.username', read_only=True)
    user_pk = serializers.IntegerField(source='user.id', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'username', 'user_pk', 'expenses_date', 'image', 'content', 'category_name', 'created_at', 'updated_at', 'price']

    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')

            return request.build_absolute_uri(obj.image.url)
        return None