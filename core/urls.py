from django.urls import path
from core.views.currency import CurrencyListCreateAPIView, CurrencyRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('currencies/', CurrencyListCreateAPIView.as_view(), name='currency-list-create'),
    path('currencies/<int:pk>/', CurrencyRetrieveUpdateDestroyAPIView.as_view(), name='currency-detail'),
]
