from datetime import datetime

from rest_framework import serializers

from app_auth.models import CustomUser
from app_merchant.models.merchant import Merchant
from services.api_key_generator import generate_key, encrypt_message
from rest_framework import serializers


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'password']


class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = [
            'id',
            'user',
            'name',
            'email',
            'contact_number',
            'api_key',
            'secret_key',
            'is_active',
            'registration_date',
        ]

        read_only_fields = ['id', 'is_active', 'api_key', 'secret_key', 'registration_date']

    def create(self, validated_data):
        secret_key = generate_key()
        api_key = encrypt_message(f"{validated_data.get('name')}_{validated_data.get('user')}", secret_key)
        return Merchant.objects.create(**validated_data, secret_key=secret_key, api_key=api_key,
                                       registration_date=datetime.now())


class MerchantUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = [
            'id',
            'user',
            'name',
            'email',
            'contact_number',
            'is_active',  # Assuming you want to allow updates to 'is_active'
        ]
        read_only_fields = ['id', 'user', 'api_key', 'secret_key', 'registration_date']

    def update(self, instance, validated_data):
        # Only update fields that are included in the request
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance
