from django.http import JsonResponse
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash, authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from dj_rest_auth.registration.views import RegisterView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser, FormParser


from .serializers import UserSerializer, LoginSerializer, CustomRegisterSerializer, UserAdditionalInfoSerializer, UserUpdateSerializer, UserDeleteSerializer, BudgetSerializer
from .models import Budget
User = get_user_model()


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
    
    
class UserAdditionalInfoView(generics.UpdateAPIView):
    serializer_class = UserAdditionalInfoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        # 디버깅을 위한 수신 데이터 로그
        # print("Received data:", request.data)
        
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            # 유효성 검사 오류 출력
            # print("Validation errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def add_info(request):
    user = request.user
    serializer = UserAdditionalInfoSerializer(user, data=request.data, partial=True)
    # print("Received data:", request.data)
    if serializer.is_valid(raise_exception=True):
        # print(serializer)
        serializer.save()
        return Response(serializer.data)


from rest_framework.parsers import MultiPartParser, FormParser

@api_view(['GET', 'PUT'])
@permission_classes([permissions.IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def update_user(request):
    user = request.user
    if request.method == 'GET':
        serializer = UserUpdateSerializer(user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            if 'profile_image' in request.FILES:
                user.profile_image = request.FILES['profile_image']
            serializer.save()
            return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_user(request):
    user = request.user
    serializer = UserDeleteSerializer(data=request.data, context={'request': request})
    if serializer.is_valid(raise_exception=True):
        user.delete()
        return Response({"detail": "사용자 계정이 성공적으로 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
    # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request, username):
    if request.user.username != username:
        return Response()({'error': 'You are not authorized to view this profile.'}, status=status.HTTP_403_FORBIDDEN)
    
    user = get_object_or_404(User, username=username)
    serializer= UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])  # 로그인된 사용자만 접근 가능
def update_budget(request):
    try:
        data = request.data
        # print("Received data:", data)

        # 요청 데이터에서 month와 year를 가져옴
        month = data.get('month')
        year = data.get('year')

        if not month or not year:
            return Response({"error": "Month and Year are required."}, status=status.HTTP_400_BAD_REQUEST)

        # 현재 로그인된 사용자의 기존 Budget 데이터 검색
        budget_instance = Budget.objects.filter(user=request.user, month=month, year=year).first()

        if budget_instance:
            # 기존 데이터가 있으면 업데이트
            serializer = BudgetSerializer(budget_instance, data=data, partial=True)
            if serializer.is_valid():
                # print("Serializer is valid for update.")
                serializer.save()  # 기존 인스턴스 업데이트
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                # print("Serializer errors during update:", serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            # 기존 데이터가 없으면 새로 생성
            serializer = BudgetSerializer(data=data)
            if serializer.is_valid():
                # print("Serializer is valid for creation.")
                serializer.save(user=request.user)  # 새 인스턴스 생성
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                # print("Serializer errors during creation:", serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        # print("Exception occurred:", str(e))  # 에러 메시지 출력
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])  # 로그인된 사용자만 접근 가능
def deduct_points(request):
    data = request.data
    amount = data.get('amount', 10)
    
    # print(request.user.point)
    if request.user.point >= amount:
        request.user.point -= amount
        request.user.save()
        return JsonResponse({'points': request.user.point})
    else:
        return JsonResponse({'error': 'Insufficient points'}, status=400)