from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app_merchant.models.merchant import Merchant
from app_payment.models.payment import Payment
from app_payment.serializers.payment import PaymentSerializer


class DepositPaymentsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        group = request.query_params.get('group', None)
        deposits = Payment.objects.filter(transaction_type='deposit')
        # if group and group=='merchant':
        #     merchant = Merchant.objects.get(pk=request.user)


        serializer = PaymentSerializer(deposits, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)