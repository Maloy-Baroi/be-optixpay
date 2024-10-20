from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from rest_framework import serializers
from app_auth.models.user import CustomUser
from django.core.cache import cache
import random


class CustomUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password']

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value, is_active=True).exists():
            raise serializers.ValidationError('A user with this email already exists.')
        return value

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        user.is_active = False  # User is inactive until OTP is verified
        user.save()

        otp = random.randint(100000, 999999)  # Generate a 6-digit OTP
        cache.set(f"otp_{user.email}", otp, timeout=300)  # Save OTP in Redis with 5 min TTL
        print(cache.get(f"otp_{user.email}"))

        # Prepare the HTML email content
        subject = 'Your One-Time Password (OTP) Code'
        context = {
            'email': user.email,
            'otp': otp,
        }
        html_message = render_to_string('emails/otp_email.html', context)
        plain_message = f'Your OTP code is {otp}'  # Fallback plain text version

        # Send OTP to user's email
        send_mail(
            subject,
            plain_message,  # Fallback to plain text message
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
            html_message=html_message,  # HTML message
        )

        return user
