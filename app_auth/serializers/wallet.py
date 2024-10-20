from rest_framework import serializers
from app_auth.models.wallet import Wallet

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id', 'user', 'wallet_type', 'wallet_phone_number', 'walter_number', 'status', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
