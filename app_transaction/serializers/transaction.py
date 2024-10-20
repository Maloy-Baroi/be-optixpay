# serializers.py
from rest_framework import serializers
from app_transaction.models.transaction import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    total_cost = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = '__all__'  # List all fields from the model if needed

    def get_total_cost(self, obj):
        return obj.calculate_total_cost()
