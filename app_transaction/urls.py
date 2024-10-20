# urls.py
from django.urls import path

from app_transaction.views.topup import TopUpListAPIView, TopUpCreateAPIView, TopUpDetailAPIView
from app_transaction.views.transaction import TransactionListCreateAPIView, TransactionDetailAPIView

urlpatterns = [
    path('transactions/', TransactionListCreateAPIView.as_view(), name='transaction-list'),
    path('transactions/<int:pk>/', TransactionDetailAPIView.as_view(), name='transaction-detail'),
    path('topups/', TopUpListAPIView.as_view(), name='topup-list'),
    path('topups/create/', TopUpCreateAPIView.as_view(), name='topup-create'),
    path('topups/<int:pk>/', TopUpDetailAPIView.as_view(), name='topup-detail'),
]
