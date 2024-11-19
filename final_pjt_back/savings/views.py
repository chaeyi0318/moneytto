from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.db.models import Q
from django.db.models import Count
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, get_list_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .serializers import SavingListSerializer, SavingRecommendSerializer
from .models import SavingProduct, SavingPeriod, SavingAmount, SavingInterest

from datetime import date


User = get_user_model()

@api_view(['GET'])
def search_savings(request):
    products = SavingProduct.objects.all()
    
    amount = request.GET.get('amount')
    period = request.GET.get('period')
    saving_method = request.GET.get('saving_method')
    institution_type = request.GET.get('institution_type')
    interest_calculation_method = request.GET.get('interest_calculation_method')
    eligibility = request.GET.get('eligibility')
    
    if amount or period:
        interest_filters = Q()
        if amount:
            amount_obj = SavingAmount.objects.filter(amount=amount).first()
            if amount_obj:
                interest_filters &= Q(savinginterest__amount=amount_obj)
        if period:
            period_obj = SavingPeriod.objects.filter(months=period).first()
            if period_obj:
                interest_filters &= Q(savinginterest__period=period_obj)
        if interest_filters:
            products = products.filter(interest_filters).distinct()
    
    if saving_method:
        products = products.filter(saving_method=saving_method)
    if institution_type:
        products = products.filter(institution_type=institution_type)
    if interest_calculation_method:
        products = products.filter(interest_calculation_method=interest_calculation_method)
    if eligibility:
        products = products.filter(eligibility=eligibility)
    
    # 정렬 옵션 처리
    sort_by = request.GET.get('sort_by', 'max_preference_rate')  # 기본값으로 최고우대금리 설정
    sort_order = request.GET.get('sort_order', 'desc')           # 기본값으로 내림차순 설정
    
    if sort_by in ['bank_name', 'product_name', 'pre_tax_interest_rate', 'post_tax_interest_rate', 'max_preference_rate', 'eligibility']:
        if sort_order == 'asc':
            products = products.order_by(sort_by)
        else:
            products = products.order_by(f'-{sort_by}')
    else:
        # 정렬 옵션이 지정되지 않았거나 잘못된 경우 최고우대금리 내림차순으로 정렬
        products = products.order_by('-max_preference_rate')
    
    if products.exists():
        result = []
        for product in products:
            serialized_product = SavingListSerializer(product).data
            
            # 세후 이자 정보 추가
            if amount and period:
                saving_interest = SavingInterest.objects.filter(
                    saving=product,
                    amount__amount=amount,
                    period__months=period
                ).first()
                
                if saving_interest and saving_interest.post_tax_interest is not None:
                    serialized_product['post_tax_interest'] = saving_interest.post_tax_interest
                else:
                    serialized_product['post_tax_interest'] = "-"
            else:
                serialized_product['post_tax_interest'] = "-"
            
            result.append(serialized_product)
        
        return Response(result, status=status.HTTP_200_OK)
    else:
        return Response({"message": "검색 결과가 없습니다."}, status=status.HTTP_200_OK)
    
# @permission_classes([IsAuthenticated])
@api_view(['POST'])
def likes(request, saving_pk):
    saving = get_object_or_404(SavingProduct, pk=saving_pk)
    
    # 찜하기 / 찜하기 취소 구분
    if request.user in saving.liked_by.all():
        saving.liked_by.remove(request.user)
        is_liked = False
    else:
        saving.liked_by.add(request.user)
        is_liked = True
    context = {
        'is_liked': is_liked,
    }
    return JsonResponse(context)

# @permission_classes([IsAuthenticated])
@api_view(['POST'])
def owns(request, saving_pk):
    saving = get_object_or_404(SavingProduct, pk=saving_pk)
    
    # 보유 / 보유 취소 구분
    if request.user in saving.owned_by.all():
        saving.owned_by.remove(request.user)
        is_owned = False
    else:
        saving.owned_by.add(request.user)
        is_owned = True
    context = {
        'is_owned': is_owned,
    }
    return JsonResponse(context)


def calculate_age(birth_date):
    today = date.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

def get_recommended_savings(user, limit=6):
    if not user.birth_date or not user.income:
        return SavingProduct.objects.none()

    user_age = calculate_age(user.birth_date)

    similar_users = User.objects.filter(
        birth_date__year__range=(user.birth_date.year - 5, user.birth_date.year + 5),
        income__range=(user.income * 0.8, user.income * 1.2)
    ).exclude(id=user.id)

    recommended_savings = SavingProduct.objects.filter(
        owned_by__in=similar_users
    ).annotate(
        ownership_count=Count('owned_by')
    ).order_by('-ownership_count')

    recommended_savings = recommended_savings.exclude(owned_by=user)

    return recommended_savings[:limit]

@api_view(['GET'])
def recommend_savings(request):
    user = request.user
    recommended_savings = get_recommended_savings(user, limit=10)
    serializer = SavingRecommendSerializer(recommended_savings, many=True)
    return Response(serializer.data)

# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import AllowAny

# @api_view(['GET'])
# @permission_classes([AllowAny])
# def recommend_savings(request):
#     # 테스트를 위해 ID가 5인 사용자를 가져옵니다.
#     user = User.objects.filter(pk=5).first()
#     if not user:
#         return Response({"error": "User with ID 5 not found"}, status=status.HTTP_404_NOT_FOUND)
    
#     if not user.birth_date or not user.income:
#         return Response({"error": "User does not have birth date or income information"}, status=status.HTTP_400_BAD_REQUEST)
    
#     recommended_savings = get_recommended_savings(user, limit=6)
#     serializer = SavingRecommendSerializer(recommended_savings, many=True)
#     return Response(serializer.data)