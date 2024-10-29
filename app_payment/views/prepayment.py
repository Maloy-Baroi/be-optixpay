import base64

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.files.base import ContentFile

from app_payment.models.currency_excahange_rate import CurrencyExchangeRate
from app_payment.models.payment import Payment
from app_payment.serializers.payment import PrePaymentSerializer, PrePaymentListSerializer


class PrePaymentCreateListAPIView(APIView):

    def get(self, request):
        try:
            data = Payment.objects.filter(transaction_type='prepayment')
            serializer = PrePaymentListSerializer(data, many=True)
            return Response({"message": "Data Found!", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        data = request.data['payload'].copy()  # Copy the request data to make it mutable

        # Handle base64 encoded image if present
        payment_screenshot_data = data.get('payment_screenshot')
        if payment_screenshot_data:
            format, imgstr = payment_screenshot_data.split(';base64,')  # Extract format and pure base64 data
            ext = format.split('/')[-1]  # Extract the extension (png, jpeg, etc.)

            # Convert base64 encoded data into an image file
            data['payment_screenshot'] = ContentFile(base64.b64decode(imgstr), name=f"temp.{ext}")

        serializer = PrePaymentSerializer(data=data)

        if serializer.is_valid():
            currency_rate = CurrencyExchangeRate.objects.get(source_from=data['currency'], converted_to='BDT')
            in_bdt = currency_rate.amount_per_unit * float(data['amount'])
            serializer.save(
                commission=0,
                after_commission=data['amount'],
                balance=data['amount'],
                in_bdt=in_bdt
            )  # Save the new Payment instance
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


