from django.db import models
from django.utils import timezone
from decimal import Decimal

from app_auth.models import CustomUser
from app_auth.models.agent_profile import AgentProfile
from core.models.base_model import BaseModel


# Payment Providers (e.g., Stripe, bKash, PayPal)
class PaymentProvider(BaseModel):
    PROVIDER_CHOICES = [
        ('bkash', 'BKash'),
        ('nagad', 'Nagad'),
        ('stripe', 'Stripe'),
        ('paypal', 'PayPal'),
        # Add more providers as necessary
    ]
    provider = models.CharField(max_length=50, choices=PROVIDER_CHOICES, unique=False, default='bkash')
    phone_number = models.CharField(max_length=20)
    password = models.CharField(max_length=255)
    api_key = models.CharField(max_length=255)
    secret_key = models.CharField(max_length=255)
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
