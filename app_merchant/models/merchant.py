from django.db import models
from django.utils.translation import gettext_lazy as _
from app_auth.models import CustomUser
from core.models.base_model import BaseModel
from core.models.history_model import HistoryMixin


class Merchant(BaseModel, HistoryMixin):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='merchants')
    name = models.CharField(_('merchant name'), max_length=255)
    email = models.EmailField(_('email address'), unique=True, null=True, blank=True)
    contact_number = models.CharField(_('contact number'), max_length=15)
    api_key = models.CharField(_('API key'), max_length=255, unique=True)
    secret_key = models.CharField(_('secret key'), max_length=255, unique=True)
    registration_date = models.DateTimeField(_('registration date'), auto_now_add=True)
