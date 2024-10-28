from django.db import models

class CryptoAddressTRC(models.Model):
    address = models.CharField(max_length=255)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.address
