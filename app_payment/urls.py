from django.urls import path

from app_payment.views.bkash import DepositBKashPayView, BkashPaymentInitiateAPIView, BkashPaymentExecuteAPIView
from app_payment.views.crypto_address_trc import CryptoAddressDetailAPIView
from app_payment.views.currency_exchange_rate import CurrencyExchangeRateAPIView
from app_payment.views.deposit import DepositPaymentsAPIView, WithdrawPaymentsAPIView, \
    WithdrawUpdatePaymentsUpdateAPIView
from app_payment.views.nagad import StartPaymentView, CompletePaymentView
from app_payment.views.payment_details import PaymentListAPIView
from app_payment.views.prepayment import PrePaymentCreateListAPIView
from app_payment.views.withdraw import PaymentCreateAPIView

urlpatterns = [
    path('bkash/grants/', DepositBKashPayView.as_view(), name='bkash-payment'),
    path('bkash/create/', BkashPaymentInitiateAPIView.as_view(), name='bkash-initiate'),
    path('bkash/execute/', BkashPaymentExecuteAPIView.as_view(), name='bkash-execute'),

    path('payment-list/', PaymentListAPIView.as_view(), name='payment-list'),

    # Nagad
    path('nagad/create/', StartPaymentView.as_view(), name='start_payment'),
    path('nagad/complete/', CompletePaymentView.as_view(), name='complete_payment'),
    # path('complete-payment/', CompletePaymentView.as_view(), name='complete_payment'),
    # path('payment-status/<str:payment_ref_id>/', CheckPaymentStatusView.as_view(), name='check_payment_status'),
    path('exchange-rates/', CurrencyExchangeRateAPIView.as_view(), name='currency_exchange_rate_list'),        # For listing and creating exchange rates
    path('crypto-addresses/', CryptoAddressDetailAPIView.as_view(), name='crypto-address-detail'),
    path('prepayment/', PrePaymentCreateListAPIView.as_view(), name='prepayment-create'),

    path('exchange-rates/<str:from_currency>/<str:to_currency>/', CurrencyExchangeRateAPIView.as_view(), name='currency_exchange_rate_detail'),  # For retrieving, updating, and deleting a specific exchange rate
    path('deposits/', DepositPaymentsAPIView.as_view(), name='deposit-payments'),
    path('withdraws/', WithdrawPaymentsAPIView.as_view(), name='deposit-payments'),
    path('withdraw/', PaymentCreateAPIView.as_view(), name='create-payment'),
    path('withdraw-update/<int:payment_id>/', WithdrawUpdatePaymentsUpdateAPIView.as_view(), name='deposit-payments'),
]
