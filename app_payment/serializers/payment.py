from rest_framework import serializers
from app_payment.models.payment import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'  # Include all fields from the Payment model
