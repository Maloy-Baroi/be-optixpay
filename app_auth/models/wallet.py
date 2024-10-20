from django.db import models
from app_auth.models.user import CustomUser


class Wallet(models.Model):
    WALLET_TYPE = [
        ('bkash', 'Bkash'),
        ('nagad', 'Nagad')
    ]
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('closed', 'Closed')
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='wallet_user')
    wallet_type = models.CharField(max_length=100, choices=WALLET_TYPE, unique=True)
    wallet_phone_number = models.CharField(max_length=15)
    walter_number = models.CharField(max_length=30, null=True, blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='active')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

