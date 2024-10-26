# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app_payment.models.currency_excahange_rate import CurrencyExchangeRate
from app_payment.serializers.currency_exchange_rate import CurrencyExchangeRateSerializer
from django.shortcuts import get_object_or_404


class CurrencyExchangeRateAPIView(APIView):
    # Retrieve all exchange rates
    def get(self, request, *args, **kwargs):
        currency_id = kwargs.get('pk')
        if currency_id:
            # Retrieve a single currency exchange rate
            exchange_rate = get_object_or_404(CurrencyExchangeRate, pk=currency_id)
            serializer = CurrencyExchangeRateSerializer(exchange_rate)
            return Response(serializer.data)
        else:
            # Retrieve all exchange rates
            exchange_rates = CurrencyExchangeRate.objects.all()
            serializer = CurrencyExchangeRateSerializer(exchange_rates, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    # Create a new exchange rate
    def post(self, request, *args, **kwargs):
        serializer = CurrencyExchangeRateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Update an existing exchange rate
    def patch(self, request, from_currency=None, to_currency=None, *args, **kwargs):
        exchange_rate = get_object_or_404(
            CurrencyExchangeRate,
            source_from=from_currency,
            converted_to=to_currency
        )
        serializer = CurrencyExchangeRateSerializer(exchange_rate, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete an exchange rate
    def delete(self, request, pk=None, *args, **kwargs):
        exchange_rate = get_object_or_404(CurrencyExchangeRate, pk=pk)
        exchange_rate.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
