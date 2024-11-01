from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app_payment.serializers.payment import PaymentCreateSerializer


class PaymentCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PaymentCreateSerializer(data=request.data)
        if serializer.is_valid():
            payment = serializer.save()
            return Response(PaymentCreateSerializer(payment).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)