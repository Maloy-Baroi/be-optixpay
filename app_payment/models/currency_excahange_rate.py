from django.db import models


class CurrencyExchangeRate(models.Model):
    source_from = models.CharField(max_length=50)
    converted_to = models.CharField(max_length=50)
    amount_per_unit = models.DecimalField(max_digits=20, decimal_places=2)

