# serializers.py
from rest_framework import serializers
from app_transaction.models.topup import TopUp

class TopUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopUp
        fields = '__all__'  # Includes all fields of the TopUp model including those inherited from Transaction
