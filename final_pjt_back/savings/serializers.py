from rest_framework import serializers
from .models import SavingProduct, SavingPeriod, SavingAmount, SavingInterest

class SavingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingProduct
        fields = '__all__'

class SavingRecommendSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingProduct
        fields = ['bank_name', 'product_name', 'saving_method', 'max_preference_rate']
        


# 리스트 시리얼라이저/ 디테일 시리얼라이저 분기할 것!
# 리스트에서는 일부 정보만 보여주고 디테일에서 모든 정보 볼 수 있도록 추후 수정
# class SavingListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SavingProduct
#         fields = (
#             'id', 
#             'bank_name', 
#             'product_name', 
#             'saving_method', 
#             'pre_tax_interest_rate', 
#             'post_tax_interest_rate', 
#             'max_preference_rate', 
#             'eligibility', 
#             'interest_calculation_method', 
#             'product_link'
#             )
        
# class SavingDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SavingProduct
#         fields = '__all__'