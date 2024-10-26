from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app_payment.utils import NagadAPIService

class StartPaymentView(APIView):
    def post(self, request):
        order_id = request.data.get('order_id')
        amount = request.data.get('amount')
        print(f"Order ID: {order_id} \namount: {amount}")
        
        nagad_service = NagadAPIService()
        result = nagad_service.initialize_payment(order_id, amount)
        
        return Response(result, status=status.HTTP_200_OK)

class CompletePaymentView(APIView):
    def post(self, request):
        payment_ref_id = request.data.get('payment_ref_id')
        amount = request.data.get('amount')
        
        nagad_service = NagadAPIService()
        result = nagad_service.complete_payment(payment_ref_id, amount)
        
        return Response(result, status=status.HTTP_200_OK)

class CheckPaymentStatusView(APIView):
    def get(self, request, payment_ref_id):
        nagad_service = NagadAPIService()
        result = nagad_service.check_payment_status(payment_ref_id)
        
        return Response(result, status=status.HTTP_200_OK)
