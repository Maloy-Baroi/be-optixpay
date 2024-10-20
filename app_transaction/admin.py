from django.contrib import admin
from app_transaction.models.topup import TopUp
from app_transaction.models.transaction import Transaction

# Register your models here.
admin.site.register(Transaction)
admin.site.register(TopUp)