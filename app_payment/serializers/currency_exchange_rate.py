# serializers.py
from rest_framework import serializers
from app_payment.models.currency_excahange_rate import CurrencyExchangeRate

class CurrencyExchangeRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyExchangeRate
        fields = ['id', 'source_from', 'converted_to', 'amount_per_unit']
