from rest_framework import serializers
from .models import SavingProduct, SavingPeriod, SavingAmount, SavingInterest

class SavingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingProduct
        fields = '__all__'
