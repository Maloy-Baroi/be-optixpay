from rest_framework import serializers
from app_auth.models import CustomUser
from app_agent.models.agent import AgentProfile, PaymentAggregatorAgent, PaymentProvider


class AgentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentProfile
        fields = ['full_name', 'email', 'date_of_birth', 'phone_number', 'nationality', 'nid_number',
                  'telegram_account', 'verification_type']


class PaymentProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentProvider
        fields = ['provider', 'phone_number', 'password', 'api_key', 'secret_key']


class PaymentAggregatorAgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentAggregatorAgent
        fields = ['agent_profile']


class PaymentProviderCreateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentProvider
        fields = [
            'bank_id',
            'name',
            'provider',
            'phone_number',
            'trx_type',
            'password',
            'api_key',
            'secret_key',
            'minimum_transaction_amount',
            'maximum_transaction_amount',
            'assigned',
            'is_active'
        ]

        extra_kwargs = {
            'bank_id': {'read_only': True},
            'assigned': {'read_only': True},
            'is_active': {'read_only': True},
        }


