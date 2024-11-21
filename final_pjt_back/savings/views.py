from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from django.utils import timezone
from django.shortcuts import render
from django.db.models import Q, Count
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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def likes(request, saving_pk):
    saving = get_object_or_404(SavingProduct, pk=saving_pk)
    
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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def owns(request, saving_pk):
    saving = get_object_or_404(SavingProduct, pk=saving_pk)
    
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
    today = timezone.now().date()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

def get_age_based_recommendations(user, limit=5):
    user_age = calculate_age(user.birth_date)
    similar_age_users = User.objects.filter(
        birth_date__year__range=(user.birth_date.year - 5, user.birth_date.year + 5)
    ).exclude(id=user.id)

    age_based_recommendations = SavingProduct.objects.filter(
        owned_by__in=similar_age_users
    ).annotate(
        ownership_count=Count('owned_by')
    ).order_by('-ownership_count')[:limit]

    return age_based_recommendations

def get_income_based_recommendations(user, limit=5):
    if user.income == 0:
        return SavingProduct.objects.order_by('-max_preference_rate')[:limit]
    
    similar_income_users = User.objects.filter(
        income__range=(user.income * 0.8, user.income * 1.2)
    ).exclude(id=user.id)

    income_based_recommendations = SavingProduct.objects.filter(
        owned_by__in=similar_income_users
    ).annotate(
        ownership_count=Count('owned_by')
    ).order_by('-ownership_count')[:limit]

    return income_based_recommendations


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommend_savings(request):
    user = request.user
    
    if not user.birth_date:
        return Response({"message": "생년월일 정보가 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)

    age_based_recommendations = get_age_based_recommendations(user)
    income_based_recommendations = get_income_based_recommendations(user)

    serializer_age = SavingRecommendSerializer(age_based_recommendations, many=True)
    serializer_income = SavingRecommendSerializer(income_based_recommendations, many=True)

    return Response({
        "age_based": serializer_age.data,
        "income_based": serializer_income.data
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def liked_savings(request):
    user = request.user
    liked_savings = user.liked_savings.all()
    serializer = SavingListSerializer(liked_savings, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)