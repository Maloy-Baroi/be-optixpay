from rest_framework import serializers
from app_payment.models.payment import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'  # Include all fields from the Payment model


class PrePaymentSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Payment
        fields = [
            "address_trc",
            "trxID",
            "transaction_type",
            "payment_screenshot",
            "amount"
        ]

    def validate_amount(self, value):
        # Add any custom validation logic here
        if float(value) <= 0.0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value


class PrePaymentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'  # Include all fields from the Payment model

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        return {
            "address_trc": ret["address_trc"],
            "OrderId": ret["trxID"],
            "transaction_type": ret["transaction_type"],
            "payment_screenshot": ret["payment_screenshot"],
            "amount": ret["amount"],
            "amount_in_bdt": ret["in_bdt"]
        }


class PaymentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['trxID', 'transaction_type', 'amount', 'commission', 'after_commission',
            'balance', 'currency', 'intent', 'merchantInvoiceNumber', 'payerType', 'payerReference',
            'customerMsisdn', 'payerAccount', 'status', 'payment_screenshot'
        ]
        extra_kwargs = {field: {'required': False} for field in fields}

