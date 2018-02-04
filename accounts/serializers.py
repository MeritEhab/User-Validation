from rest_framework import serializers

from accounts.models import Accounts
from phonenumber_field.serializerfields import PhoneNumberField



class AccountSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    birth_date = serializers.DateField(format="%Y-%m-%d")
    phone_number = PhoneNumberField(required=True)

    class Meta:
        model = Accounts
        fields = ('first_name', 'last_name', 'country_code', 'phone_number',
         'gender', 'birth_date', 'avatar', 'email')

