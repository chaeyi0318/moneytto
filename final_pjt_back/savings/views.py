from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from django.shortcuts import render
from django.shortcuts import get_object_or_404, get_list_or_404

from .models import SavingProduct, SavingPeriod, SavingAmount, SavingInterest
from .serializers import SavingListSerializer

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