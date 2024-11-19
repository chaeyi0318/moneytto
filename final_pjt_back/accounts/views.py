from django.shortcuts import render
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer, LoginSerializer, CustomRegisterSerializer
from dj_rest_auth.registration.views import RegisterView
from django.contrib.auth import authenticate

class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer
    
# Create your views here.
@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        serializer = CustomRegisterSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save(request)

            # 토큰 생성 및 반환
            token, created = Token.objects.get_or_create(user=user)

            response_data = serializer.data
            response_data.pop('password', None)
            response_data['token'] = token.key  # 토큰 추가

            return Response(response_data, status=status.HTTP_201_CREATED)
        

@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            auth_login(request, user)

            token, created = Token.objects.get_or_create(user=user)
            
            return Response({
                'token': token.key,
                'user': serializer.data
                }, status=status.HTTP_200_OK)
        
@api_view(['POST'])
def logout(request):
    try:
        # 현재 요청의 사용자 토큰을 가져와 삭제
        token = Token.objects.get(user=request.user)
        token.delete()

        # Django의 세션 로그아웃 처리
        auth_logout(request)

        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
    except Token.DoesNotExist:
        return Response({"detail": "Invalid token or user not logged in."}, status=status.HTTP_400_BAD_REQUEST)