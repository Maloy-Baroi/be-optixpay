# models.py
from django.db import models
from django.utils import timezone

from app_agent.models.agent import PaymentProvider
from core.models.base_model import BaseModel
from core.models.history_model import HistoryMixin


class Transaction(BaseModel, HistoryMixin):
    # Original fields
    merchant_order_id = models.CharField(max_length=100, unique=True)
    pgw_order_id = models.CharField(max_length=100, unique=True)
    merchant_id = models.CharField(max_length=50)
    merchant_name = models.CharField(max_length=255)
    user_id = models.CharField(max_length=50)
    bank_name = models.CharField(max_length=100)
    bank_trx_id = models.CharField(max_length=100, unique=True)
    request_amount = models.DecimalField(max_digits=20, decimal_places=2)
    received_amount = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    request_currency = models.CharField(max_length=10)
    base_currency = models.CharField(max_length=10)
    paid_at = models.DateTimeField(null=True, blank=True)
    agent_id = models.CharField(max_length=50, null=True, blank=True)
    agent_bank_id = models.CharField(max_length=50, null=True, blank=True)
    provider = models.ForeignKey(PaymentProvider, on_delete=models.SET_NULL, null=True)
    sender_bank_no = models.CharField(max_length=50)
    receiver_bank_no = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=[
        ('awaiting', 'Awaiting'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
    ], default='pending')
    commission = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    # Additional fields
    transaction_type = models.CharField(max_length=20, choices=[
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('transfer', 'Transfer'), 
        ('payment', 'Payment'),
    ], default='payment', help_text="Type of the transaction.")

    description = models.TextField(null=True, blank=True, help_text="Description or note about the transaction.")
    
    is_refundable = models.BooleanField(default=False, help_text="Indicates if the transaction is refundable.")
    refund_amount = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Amount that can be refunded if applicable.")

    transaction_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, help_text="Fee charged for the transaction.")
    
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, help_text="Exchange rate applied if different currencies are involved.")
    
    processed_by = models.CharField(max_length=100, null=True, blank=True, help_text="Name or ID of the system or user who processed the transaction.")
    
    # Tracking timestamps for various states
    cancelled_at = models.DateTimeField(null=True, blank=True, help_text="Timestamp when the transaction was cancelled.")
    refunded_at = models.DateTimeField(null=True, blank=True, help_text="Timestamp when the transaction was refunded.")
    
    # Metadata
    metadata = models.JSONField(null=True, blank=True, help_text="Additional metadata for the transaction in JSON format (requires PostgreSQL).")

    class Meta:
        ordering = ['-created_at']
        db_table = 'transaction'
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"

    def __str__(self):
        return f"Transaction {self.merchant_order_id} - {self.status}"
    
    def is_completed(self):
        """ Check if the transaction is completed """
        return self.status == 'completed'
    
    def calculate_total_cost(self):
        """ Calculate the total cost including commission and transaction fee """
        return (self.request_amount + self.commission + self.transaction_fee) if self.request_amount else 0.0
