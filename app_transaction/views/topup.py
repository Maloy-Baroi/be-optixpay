# views.py
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app_transaction.models.topup import TopUp
from app_transaction.serializers.topup import TopUpSerializer

class TopUpCreateAPIView(APIView):
    """
    Create a new TopUp transaction.
    """
    def post(self, request, format=None):
        serializer = TopUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TopUpListAPIView(APIView):
    """
    List all TopUp transactions.
    """
    def get(self, request, format=None):
        topups = TopUp.objects.all()
        serializer = TopUpSerializer(topups, many=True)
        return Response(serializer.data)

class TopUpDetailAPIView(APIView):
    """
    Retrieve, update or delete a TopUp transaction.
    """
    def get_object(self, pk):
        try:
            return TopUp.objects.get(pk=pk)
        except TopUp.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        topup = self.get_object(pk)
        serializer = TopUpSerializer(topup)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        topup = self.get_object(pk)
        serializer = TopUpSerializer(topup, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        topup = self.get_object(pk)
        topup.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
