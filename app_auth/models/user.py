from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, Group, Permission
from django.db import models
from django.core.validators import RegexValidator


# app_auth/models.py
class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The email field must be set!")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError("Superuser must have is_staff=True")
        if not extra_fields.get('is_superuser'):
            raise ValueError("Superuser must have is_superuser=True")

        return self._create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone_regex = RegexValidator(
        regex=r'^\+?880\d{10}$',
        message="Phone number must be entered in the format: '+880xxxxxxxxxx'."
    )
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    create_date = models.DateTimeField(auto_now_add=True)
    write_date = models.DateTimeField(auto_now=True)
    create_uid = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name='created_users')
    write_uid = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL,
                                  related_name='written_users')
    is_staff = models.BooleanField(default=False)  # Add this field
    is_active = models.BooleanField(default=True)  # This field is also often required
    new_user = models.BooleanField(default=True)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Custom related name to avoid clash
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',  # Custom related name to avoid clash
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def save(self, *args, **kwargs):
        # Check if the password needs to be hashed
        if self._password_is_plain(self.password):
            self.set_password(self.password)
        super().save(*args, **kwargs)

    def _password_is_plain(self, password):
        """
        Helper method to check if a password is already hashed.
        Django hashed passwords start with a hash identifier.
        """
        return not password.startswith("pbkdf2_") and not password.startswith("argon2$")

    def set_password(self, raw_password):
        """
        Sets the user’s password to the given raw string, taking care of the hashing.
        """
        super().set_password(raw_password)


