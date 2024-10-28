from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app_payment.models.crypto_address_trc import CryptoAddressTRC
from app_payment.serializers.crypto_address_trc import CryptoAddressTRCSerializer


class CryptoAddressDetailAPIView(APIView):
    """
    View to retrieve a specific crypto address by ID.
    """
    def get(self, request):
        address = get_object_or_404(CryptoAddressTRC, status=True)
        serializer = CryptoAddressTRCSerializer(address)
        return Response(serializer.data, status=status.HTTP_200_OK)