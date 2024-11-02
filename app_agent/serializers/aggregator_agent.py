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
            'id',
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
            'id': {'read_only': True},
            'bank_id': {'read_only': True},
            'assigned': {'read_only': True},
            'is_active': {'read_only': True},
        }

    def create(self, validated_data):
        # Exclude `bank_id` since it has a default value and should not be manually set
        validated_data.pop('bank_id', None)
        return super().create(validated_data)


class PaymentProviderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentProvider
        fields = '__all__'


class AgentProfileListSerializer(serializers.ModelSerializer):
    agent_bank_details = serializers.SerializerMethodField()
    class Meta:
        model = AgentProfile
        fields = [
            'id', 'user', 'full_name', 'email', 'date_of_birth', 'phone_number',
            'nationality', 'nid_number', 'telegram_account', 'verification_type',
            'front_side_document', 'back_side_document', 'selfie_with_document',
            'agent_bank_details'
        ]

    def get_agent_bank_details(self, obj):
        obj_id = obj.id
        providers = PaymentAggregatorAgent.objects.filter(agent_profile=obj_id)
        all_providers = []
        for provider in providers:
            banks = provider.providers.all()
            bank_serializer = PaymentProviderCreateListSerializer(banks, many=True)
            all_providers.append(bank_serializer.data)

        return all_providers

