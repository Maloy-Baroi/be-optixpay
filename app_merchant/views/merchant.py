import random

from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from django.db import transaction
from app_agent.models.agent import PaymentAggregatorAgent
from app_merchant.models.merchant import Merchant
from app_merchant.serializers.merchant import MerchantSerializer, MerchantUpdateSerializer, CustomUserSerializer
from services.admin_checker import IsSuperAdmin


class CreateUserAndMerchantAPIView(APIView):
    @transaction.atomic
    def post(self, request):
        user_data = request.data.get('user')
        merchant_data = request.data.get('merchant')

        # Serialize and validate user data
        user_serializer = CustomUserSerializer(data=user_data)
        if user_serializer.is_valid():
            # Set hashed password
            user_serializer.validated_data['password'] = make_password(user_serializer.validated_data['password'])
            user = user_serializer.save()

            # Set the user reference in merchant data
            merchant_data['user'] = user.id
            merchant_serializer = MerchantSerializer(data=merchant_data)

            if merchant_serializer.is_valid():
                merchant_serializer.save()
                return Response({
                    "user": user_serializer.data,
                    "merchant": merchant_serializer.data
                }, status=status.HTTP_201_CREATED)
            else:
                return Response(merchant_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MerchantCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def get(self, request):
        queryset = Merchant.objects.all()
        serializer = MerchantSerializer(queryset, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = MerchantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MerchantRetrieveAPIView(APIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def get(self, request, pk):
        try:
            merchant = Merchant.objects.get(pk=pk)
        except Merchant.DoesNotExist:
            raise NotFound('A merchant with this ID does not exist.')
        serializer = MerchantSerializer(merchant)
        return Response(serializer.data)


class MerchantUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def patch(self, request, pk):
        try:
            merchant = Merchant.objects.get(pk=pk)
        except Merchant.DoesNotExist:
            raise NotFound('A merchant with this ID does not exist.')
        serializer = MerchantUpdateSerializer(merchant, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MerchantDestroyAPIView(APIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def delete(self, request, pk):
        try:
            merchant = Merchant.objects.get(pk=pk)
        except Merchant.DoesNotExist:
            raise NotFound('A merchant with this ID does not exist.')
        merchant.soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class VerifyMerchantView(APIView):
    permission_classes = [IsAuthenticated]
    queryset = Merchant.objects.all()

    def post(self, request):
        try:
            api_key = request.data.get('api_key')
            secret_key = request.data.get('secret_key')
            payment_method = request.data.get('payment_method')
            print("Payment Method: ", payment_method)
            merchant = Merchant.objects.get(api_key=api_key, secret_key=secret_key)

            if merchant:
                # Fetch a payment aggregator agent that supports the provided payment_method (provider)
                selected_agent_ids = PaymentAggregatorAgent.objects.filter(
                    providers__is_active=True
                ).values_list('id', flat=True)

                selected_agent_id = random.choice(selected_agent_ids)

                selected_agent = PaymentAggregatorAgent.objects.get(id=selected_agent_id)

                if selected_agent:
                    # Retrieve provider for the specific payment_method
                    provider = selected_agent.providers.all().filter(provider__iexact=payment_method)

                    if provider.exists():
                        # Safe to access the first element as the queryset is not empty
                        provider_data = provider.first()

                        # Return a response with the provider name and agent data, without exposing sensitive keys
                        agent_data = {
                            'id': selected_agent.id,
                            'agent_name': selected_agent.agent_profile.full_name,
                            'provider_key': provider_data.api_key,
                            'provider_secret': provider_data.secret_key,
                            'provider_phone_number': provider_data.phone_number,
                            'provider_password': provider_data.password,
                        }

                        return Response({
                            'message': 'Merchant is verified.',
                            'agent_data': agent_data,
                            'my_merxt': merchant.id
                        }, status=status.HTTP_200_OK)
                    else:
                        return Response({'message': f'No provider found for payment method: {payment_method}'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'Merchant is not verified'}, status=status.HTTP_400_BAD_REQUEST)
        except Merchant.DoesNotExist:
            return Response({'message': 'Merchant is not found!'}, status=status.HTTP_404_NOT_FOUND)

