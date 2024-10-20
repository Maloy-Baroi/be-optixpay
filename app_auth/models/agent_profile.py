from django.db import models
from django.core.exceptions import ValidationError
from app_auth.models.user import CustomUser
from core.models.base_model import BaseModel
from services.global_variables import COUNTRIES, VERIFICATION_TYPE


def validate_nid_number(value):
    if len(value) not in [10, 13, 17]:
        raise ValidationError(
            'NID number must be either 10, 13, or 17 characters long.'
        )


class AgentProfile(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='profile_user')
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, null=True, blank=True)
    date_of_birth = models.DateField(default="2000-01-01")
    phone_number = models.CharField(max_length=15, default="+8801888888888")
    nationality = models.CharField(max_length=100, choices=COUNTRIES, default="Bangladesh")
    nid_number = models.CharField(
            max_length=17,
            validators=[validate_nid_number],
            unique=True
        )
    telegram_account = models.CharField(max_length=20) # D Type in sample profile
    verification_type = models.CharField(max_length=20, choices=VERIFICATION_TYPE, default='nid')
    front_side_document = models.ImageField(upload_to='uploads/verification/front_side/%Y/%m/%d', null=True)
    back_side_document = models.ImageField(upload_to='uploads/verification/back_side/%Y/%m/%d', null=True)
    selfie_with_document = models.ImageField(upload_to='uploads/verification/selfie_with_document/%Y/%m/%d', null=True)

