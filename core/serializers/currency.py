from rest_framework import serializers
from core.models.currency import Currency


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['id', 'name', 'symbol', 'short_name']

        extra_kwargs = {
            'id': {'read_only': True}
        }
