from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app_agent.models.agent import PaymentAggregatorAgent
from app_auth.models.agent_profile import AgentProfile
from app_merchant.models.merchant import Merchant
from app_payment.models.payment import Payment
from app_payment.serializers.payment import PaymentSerializer, PaymentUpdateSerializer


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


class WithdrawPaymentsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            agent_profile = AgentProfile.objects.get(user=user)
            aggregator = PaymentAggregatorAgent.objects.get(agent_profile=agent_profile)
            banks = aggregator.providers.all()
            phone_numbers = [bank.phone_number for bank in banks]
            print(phone_numbers)
            group = request.query_params.get('group', None)
            withdraws = Payment.objects.filter(transaction_type='withdraw')
            if group and group != 'admin':
                withdraws = withdraws.filter(payerReference="")

            serializer = PaymentSerializer(withdraws, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"message": "No data found!"}, status=status.HTTP_404_NOT_FOUND)


class WithdrawUpdatePaymentsUpdateAPIView(APIView):
    # permission_classes = [IsAuthenticated]  # Assuming you require authentication

    def patch(self, request, payment_id):
        try:
            payment = Payment.objects.get(id=payment_id)
            print("Payment: ", payment)
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PaymentUpdateSerializer(payment, data=request.data, partial=True)  # Allow partial update
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
