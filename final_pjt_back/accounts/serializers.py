from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import User
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'profile_image', 'nickname']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            profile_image=validated_data.get('profile_image'),
            nickname=validated_data['nickname']
        )
        user.set_password(validated_data['password'])  # 비밀번호 해싱
        user.save()
        return user
    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if user is None:
                raise serializers.ValidationError('Invalid login credentials')
        
        data['user'] = user
        return data


    def to_representation(self, instance):
        user = instance['user']
        return {
            'id': user.id,
            'username': user.username,
            'nickname': user.nickname
        }
    
class CustomRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField(max_length=30)
    profile_image = serializers.ImageField(required=False)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['nickname'] = self.validated_data.get('nickname', None)
        data['profile_image'] = self.validated_data.get('profile_image', None)

        return data

    def save(self, request):
        user = super().save(request)
        user.nickname = self.cleaned_data.get('nickname', None)
        user.profile_image = self.cleaned_data.get('profile_image', None)
        user.save()
        return user
    
class UserAdditionalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['birth_date', 'assets', 'income']

class UserUpdateSerializer(serializers.ModelSerializer):
    profile_image = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'nickname', 'birth_date', 'income', 'assets', 'profile_image']

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'profile_image' and value:
                instance.profile_image = value
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance

# class UserUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['username', 'profile_image', 'nickname', 'birth_date', 'income', 'assets', 'point']
#         extra_kwargs = {
#             'username': {'read_only': True},
#             'point': {'read_only': True}
#         }
        
class UserDeleteSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True)

    def validate_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")
        return value