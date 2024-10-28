import base64

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.files.base import ContentFile

from app_payment.serializers.payment import PrePaymentSerializer


class PrePaymentCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data.copy()  # Copy the request data to make it mutable

        # Handle base64 encoded image if present
        payment_screenshot_data = data.get('payment_screenshot')
        if payment_screenshot_data:
            format, imgstr = payment_screenshot_data.split(';base64,')  # Extract format and pure base64 data
            ext = format.split('/')[-1]  # Extract the extension (png, jpeg, etc.)

            # Convert base64 encoded data into an image file
            data['payment_screenshot'] = ContentFile(base64.b64decode(imgstr), name=f"temp.{ext}")

        serializer = PrePaymentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()  # Save the new Payment instance
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)