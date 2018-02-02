from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

from django.db import models


class Accounts(AbstractUser):

    gender_options = (
        ('M', ('Male')),
        ('F', ('Female'))
    )
    country_code = models.CharField(max_length=2, verbose_name=("Country Code"), null=False, blank=False)
    phone_number = PhoneNumberField(null=False, blank=False)
    gender = models.CharField(max_length=1, choices=gender_options, null=False, blank=False)
    avatar = models.ImageField(verbose_name=("Avatar"), null=False, blank=False)
