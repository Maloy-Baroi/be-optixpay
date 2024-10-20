from django.db import models
from core.models.base_model import BaseModel
from core.models.history_model import HistoryMixin


class Currency(BaseModel, HistoryMixin):
    name = models.CharField(max_length=100, unique=True)
    symbol = models.CharField(max_length=10, unique=True)
    short_name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.name} ({self.short_name})"
