from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.authtoken.models import Token


class AccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone_number, password, is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given phone_number and password.
        """
        if not phone_number:
            raise ValueError('The given phone number must be set')
        user = self.model(phone_number=phone_number, is_staff=is_staff, is_superuser=is_superuser, is_active=True, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, password=None, **extra_fields):
        return self._create_user(phone_number, password, False, False, **extra_fields)

    def create_superuser(self, phone_number, password, **extra_fields):
        return self._create_user(phone_number, password, True, True, **extra_fields)


class Accounts(AbstractBaseUser, PermissionsMixin):

    gender_options = (
        ('M', ('Male')),
        ('F', ('Female'))
    )
    first_name = models.CharField(max_length=255, null=False, blank=False)
    last_name = models.CharField(max_length=255, null=False, blank=False)
    country_code = models.CharField(max_length=2, null=False, blank=False)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    gender = models.CharField(max_length=1, choices=gender_options, null=False, blank=False)
    avatar = models.ImageField(null=False, blank=False)
    email = models.EmailField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    birth_date = models.DateField(auto_now=False, auto_now_add=False)

    USERNAME_FIELD = 'phone_number'
    objects = AccountManager()

    def get_short_name(self):
        return self.first_name

    def __unicode__(self):
        return str(self.phone_number)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
