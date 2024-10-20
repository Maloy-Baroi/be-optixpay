from django.db import models
from app_transaction.models.transaction import Transaction


class TopUp(Transaction):
    crypto_address = models.CharField(max_length=255, null=True, blank=True)  # For crypto transactions
    tx_id = models.CharField(max_length=255, null=True, blank=True)  # Transaction ID in the blockchain
    payment_screenshot = models.FileField(upload_to='uploads/verification/payment_screenshot/%Y/%m/%d', null=True, blank=True)