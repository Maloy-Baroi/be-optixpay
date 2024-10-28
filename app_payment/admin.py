from django.contrib import admin

from app_payment.models.crypto_address_trc import CryptoAddressTRC
from app_payment.models.payment import Payment
from app_payment.models.currency_excahange_rate import CurrencyExchangeRate

# Register your models here.
admin.site.register(Payment)
admin.site.register(CurrencyExchangeRate)
admin.site.register(CryptoAddressTRC)
