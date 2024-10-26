import os
import random

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from app_payment.utils import Nagad

# from app_payment.utils import NagadAPIService
# Access the environment variables
credentials = {
    "merchantID": os.getenv("MERCHANT_ID"),
    "isSandbox": os.getenv("IS_SANDBOX") == "True",
    "pgPublicKey": os.getenv("PG_PUBLIC_KEY"),
    "merchantPrivateKey": os.getenv("MERCHANT_PRIVATE_KEY")
}


class StartPaymentView(APIView):
    def post(self, request):
        try:
            order_id = request.data.get('order_id')
            amount = request.data.get('amount')

            nagad = Nagad(credentials)
            response = nagad.regular_payment(order_id=order_id, amount=amount)

            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# class CompletePaymentView(APIView):
#     def post(self, request):
#         payment_ref_id = request.data.get('payment_ref_id')
#         amount = request.data.get('amount')
#
#         nagad_service = NagadAPIService()
#         result = nagad_service.complete_payment(payment_ref_id, amount)
#
#         return Response(result, status=status.HTTP_200_OK)
#
# class CheckPaymentStatusView(APIView):
#     def get(self, request, payment_ref_id):
#         nagad_service = NagadAPIService()
#         result = nagad_service.check_payment_status(payment_ref_id)
#
#         return Response(result, status=status.HTTP_200_OK)
