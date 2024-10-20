# app_auth/serializers.py

from rest_framework import serializers
from app_auth.models.user import CustomUser  # Correct path to the CustomUser model
from django.contrib.auth.models import Group, Permission

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password', 'create_date', 'write_date', 'is_staff', 'is_active']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            password=validated_data['password'],
            email=validated_data.get('email', ''),
            is_staff=validated_data.get('is_staff', False),
            is_active=validated_data.get('is_active', True),
        )
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        instance.is_active = validated_data.get('is_active', instance.is_active)

        if 'password' in validated_data:
            instance.set_password(validated_data['password'])

        instance.save()
        return instance


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename', 'content_type']
