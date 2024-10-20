from django.db import models

from app_merchant.models.merchant import Merchant
from core.models.base_model import BaseModel
from core.models.history_model import HistoryMixin


class Payment(BaseModel, HistoryMixin):
    STATUS_CHOICES = [
        ('pending', 'pending'),
        ('successful', 'successful'),
        ('rejected', 'rejected'),
        ('failed', 'failed'),
    ]
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    paymentID = models.CharField(max_length=100, unique=True, null=True, blank=True)  # Assuming paymentID is unique
    paymentMethod = models.CharField(max_length=50, null=True, blank=True)
    trxID = models.CharField(max_length=100, unique=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, null=True, blank=True)
    intent = models.CharField(max_length=50, null=True, blank=True)
    merchantInvoiceNumber = models.CharField(max_length=100, null=True, blank=True)
    payerType = models.CharField(max_length=50, null=True, blank=True)
    payerReference = models.CharField(max_length=15, null=True, blank=True)  # Assuming it's a phone number reference
    customerMsisdn = models.CharField(max_length=15, null=True, blank=True)
    payerAccount = models.CharField(max_length=15, null=True, blank=True)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default="pending")

    def __str__(self):
        return f"Payment {self.paymentID} - Status: {self.status}"
