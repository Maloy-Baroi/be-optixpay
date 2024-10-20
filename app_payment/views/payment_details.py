from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app_payment.models.payment import Payment
from app_payment.serializers.payment import PaymentSerializer


class PaymentListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_description="Retrieve an Agent Profile")
    def get(self, request):
        date_from = request.query_params.get('date_from', None)
        date_to = request.query_params.get('date_to', None)
        user = request.user
        user_group = user.groups.all()
        if user_group and "agent" in user_group:
            payments = Payment.objects.all().order_by('-id')
        elif user_group and "merchant" in user_group:
            payments = Payment.objects.filter(merchant__user=user).order_by('-id')
        else:
            payments = Payment.objects.all().order_by('-id')

        if date_from and date_to:
            payments = payments.filter(updated_at__gte=date_from, updated_at__lte=date_to)
        serializer = PaymentSerializer(payments, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

