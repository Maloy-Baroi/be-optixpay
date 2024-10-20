from datetime import datetime

from django.db import models
from simple_history.models import HistoricalRecords
from django.forms.models import model_to_dict
from app_auth.models.user import CustomUser


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().all()


class BaseModel(models.Model):
    IS_ACTIVE_VALUeS = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('hold', 'Hold'),
        ('soft_deleted', 'Soft Deleted'),
    ]

    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL,
                                   null=True, related_name='%(class)s_created')
    updated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL,
                                   null=True, related_name='%(class)s_updated')

    is_active = models.CharField(max_length=20, choices=IS_ACTIVE_VALUeS, default='inactive')
    version = models.IntegerField(default=1)

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    def soft_delete(self, update_user=None):
        self.is_active = 'soft_deleted'
        if update_user is not None:
            self.updated_by = update_user
        self.save()
