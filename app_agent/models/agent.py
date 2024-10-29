from django.db import models
from django.utils import timezone
from decimal import Decimal

from app_auth.models import CustomUser
from app_auth.models.agent_profile import AgentProfile
from core.models.base_model import BaseModel


# Payment Providers (e.g., Stripe, bKash, PayPal)
class PaymentProvider(BaseModel):
    PROVIDER_CHOICES = [
        ('bkash', 'bkash'),
        ('nagad', 'nagad'),
        # Add more providers as necessary
    ]
    bank_id = models.CharField(max_length=200, default='123456')
    # named bank name
    name = models.CharField(max_length=200)
    provider = models.CharField(max_length=50, choices=PROVIDER_CHOICES, unique=False, default='bkash')
    # bank number
    phone_number = models.CharField(max_length=20)
    # Transaction Type
    trx_type = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    api_key = models.CharField(max_length=255)
    secret_key = models.CharField(max_length=255)
    minimum_transaction_amount = models.DecimalField(max_digits=10, decimal_places=2)
    maximum_transaction_amount = models.DecimalField(max_digits=10, decimal_places=2)
    assigned = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)  # To toggle active status of provider

    def __str__(self):
        return f"{self.provider}-{self.phone_number}"

    def process_payment(self, amount, currency="BDT"):
        """
        Method to be overridden by specific provider logic.
        Ideally, you'd implement provider-specific APIs here.
        """
        raise NotImplementedError("You need to implement provider-specific payment logic")


# Payment Aggregator Agent
class PaymentAggregatorAgent(BaseModel):
    agent_profile = models.ForeignKey(AgentProfile, on_delete=models.CASCADE, related_name='agent_profile')
    providers = models.ManyToManyField(PaymentProvider, related_name='agents')

    def __str__(self):
        return self.agent_profile.full_name
