from rest_framework import serializers
from app_auth.models.agent_profile import AgentProfile

class AgentProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentProfile
        fields = [
            'full_name',
            'email',
            'date_of_birth',
            'phone_number',
            'nationality',
            'nid_number',
            'telegram_account',
            'verification_type',
            'front_side_document',
            'back_side_document'
        ]
        extra_kwargs = {
            'email': {'required': False},
            'telegram_account': {'required': False},
        }

    def validate_email(self, value):
        """
        Add custom validation for the email field to ensure uniqueness
        """
        if AgentProfile.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def validate_phone_number(self, value):
        """
        Add custom validation for phone numbers if needed
        """
        # You can add your phone number format validation here
        return value

    def create(self, validated_data):
        profile = AgentProfile.objects.create(**validated_data)
        return profile


class AgentProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentProfile
        fields = '__all__'
        read_only_fields = ('user',)


class AgentProfileRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentProfile
        fields = '__all__'
