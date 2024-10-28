from rest_framework.serializers import ModelSerializer

from app_payment.models.crypto_address_trc import CryptoAddressTRC


class CryptoAddressTRCSerializer(ModelSerializer):
    class Meta:
        model = CryptoAddressTRC
        fields = ['id', 'address', 'status']
