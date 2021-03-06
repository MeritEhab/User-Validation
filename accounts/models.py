from __future__ import unicode_literals

from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField


class AccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone_number, birth_date, password, is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given phone_number birth date, and password.
        """
        if not phone_number:
            raise ValueError('The given phone number must be set')
        if not birth_date:
            raise ValueError('The given birth date must be set')
        user = self.model(phone_number=phone_number, birth_date=birth_date,
         is_staff=is_staff, is_superuser=is_superuser, is_active=True, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, birth_date, password=None, **extra_fields):
        return self._create_user(phone_number, birth_date, password, False, False, **extra_fields)

    def create_superuser(self, phone_number, birth_date, password, **extra_fields):
        return self._create_user(phone_number, birth_date, password, True, True, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin):

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
    REQUIRED_FIELDS = ['birth_date', ]

    objects = AccountManager()

    def get_short_name(self):
        return self.first_name

    def __unicode__(self):
        return str(self.phone_number)


class Status(models.Model):
    status = models.CharField(max_length=255, null=False, blank=False)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __unicode__(self):
        return str(self.user) + ' ' + self.status
