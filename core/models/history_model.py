# mixins.py
from django.db import models
from simple_history.models import HistoricalRecords

class HistoryMixin(models.Model):
    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True

