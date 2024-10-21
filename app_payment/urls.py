from django.urls import path
from app_payment.views.bkash import DepositBKashPayView, BkashPaymentInitiateAPIView, BkashPaymentExecuteAPIView
from app_payment.views.nagad import NagadPaymentInitiateView, NagadPaymentConfirmView
from app_payment.views.payment_details import PaymentListAPIView

urlpatterns = [
    path('bkash/grants/', DepositBKashPayView.as_view(), name='bkash-payment'),
    path('bkash/create/', BkashPaymentInitiateAPIView.as_view(), name='bkash-initiate'),
    path('bkash/execute/', BkashPaymentExecuteAPIView.as_view(), name='bkash-execute'),

    path('payment-list/', PaymentListAPIView.as_view(), name='payment-list'),

    # Nagad
    path('nagad/initiate/', NagadPaymentInitiateView.as_view(), name='nagad-initiate'),
    path('nagad/confirm/', NagadPaymentConfirmView.as_view(), name='nagad-confirm'),
]
