# payments/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from services.nagad import NagadPaymentService

class NagadPaymentInitiateView(APIView):
    def post(self, request, *args, **kwargs):
        order_id = request.data.get("order_id")
        amount = request.data.get("amount")
        if not order_id or not amount:
            return Response({"error": "Missing order_id or amount"}, status=status.HTTP_400_BAD_REQUEST)

        service = NagadPaymentService()
        result = service.initiate_payment(amount, order_id)

        print(result)

        if "error" in result:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        return Response(result, status=status.HTTP_200_OK)


class NagadPaymentConfirmView(APIView):
    def post(self, request, *args, **kwargs):
        payment_ref = request.data.get("payment_ref")
        if not payment_ref:
            return Response({"error": "Missing payment_ref"}, status=status.HTTP_400_BAD_REQUEST)

        service = NagadPaymentService()
        result = service.confirm_payment(payment_ref)

        if "error" in result:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        return Response(result, status=status.HTTP_200_OK)
