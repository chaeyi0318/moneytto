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