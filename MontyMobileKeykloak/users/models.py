import uuid
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.db import models, transaction
from django.utils import timezone
from model_utils.fields import StatusField
from model_utils.models import TimeStampedModel


from users.choices import ROLE


class UserManager(BaseUserManager):
    """"""

    def create_user(self, **extra_fields):
        """create and save a new user"""
        email = extra_fields.get('email')

        if not email:
            raise ValueError('Users must have an email address')
        extra_fields['email'] = self.normalize_email(email)
        user = self.model(**extra_fields)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """create and save a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """custom user model that support using email instead of username"""
    ROLE = ROLE
    keycloak_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    role = StatusField(choices_name='ROLE', default=ROLE.normal_user)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'