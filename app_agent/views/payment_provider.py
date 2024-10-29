import random
import uuid

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from app_agent.models.agent import PaymentProvider
from app_agent.serializers.aggregator_agent import PaymentProviderCreateListSerializer

class PaymentProviderListCreateAPIView(APIView):
    """
    View to list all payment providers and create a new payment provider.
    """
    def get(self, request):
        # List all payment providers
        providers = PaymentProvider.objects.all()
        serializer = PaymentProviderCreateListSerializer(providers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # Create a new payment provider
        serializer = PaymentProviderCreateListSerializer(data=request.data)
        bank_id = f"ag-{uuid.uuid4()}"
        if serializer.is_valid():
            serializer.save(bank_id=bank_id, assign=False, is_active=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PaymentProviderDetailAPIView(APIView):
    """
    View to retrieve, update, or delete a specific payment provider.
    """
    def get_object(self, pk):
        # Helper method to get the object by primary key
        return get_object_or_404(PaymentProvider, pk=pk)

    def get(self, request, pk):
        # Retrieve a payment provider by ID
        provider = self.get_object(pk)
        serializer = PaymentProviderCreateListSerializer(provider)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        # Update an existing payment provider
        provider = self.get_object(pk)
        serializer = PaymentProviderCreateListSerializer(provider, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        # Delete a payment provider
        provider = self.get_object(pk)
        provider.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
