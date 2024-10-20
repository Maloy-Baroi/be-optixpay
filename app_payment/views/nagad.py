# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from services.nagad import initiate_payment, verify_payment

class StartPaymentAPIView(APIView):
    def post(self, request):
        # Extracting data from the request body
        amount = request.data.get('amount')
        order_id = request.data.get('order_id')

        # Initiate the payment
        payment_response = initiate_payment(amount, order_id)

        # If the initiation is successful, return the payment URL
        if payment_response.get('status') == 'success':
            return Response({
                'message': 'Payment initiation successful',
                'payment_url': payment_response.get('payment_url')
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': 'Payment initiation failed',
                'error': payment_response.get('error', 'An error occurred')
            }, status=status.HTTP_400_BAD_REQUEST)


class PaymentCallbackAPIView(APIView):
    def get(self, request):
        # Extract payment_id from query parameters
        payment_id = request.query_params.get('payment_id')

        # Verify the payment
        verification_response = verify_payment(payment_id)

        # If the verification is successful, handle the success logic
        if verification_response.get('status') == 'success':
            return Response({
                'message': 'Payment verified successfully',
                'data': verification_response
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': 'Payment verification failed',
                'error': verification_response.get('error', 'Verification error')
            }, status=status.HTTP_400_BAD_REQUEST)
