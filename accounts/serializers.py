from accounts.models import Account, Status

from datetime import datetime
from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError

from phonenumber_field.serializerfields import PhoneNumberField


class AccountSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    birth_date = serializers.DateField(format="%Y-%m-%d")
    phone_number = PhoneNumberField(required=True)

    def validate(self, data):
        today = datetime.now().date()
        age = today.year - data['birth_date'].year - ((today.month, today.day) < (data['birth_date'].month, data['birth_date'].day))
        if data['birth_date'] >= today:
            raise ValidationError("Birthdate must be in the past")
        if age < 13:
            raise ValidationError("You must be at least 13 years old to register")

        return data

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'password', 'country_code',
         'phone_number', 'gender', 'birth_date', 'avatar', 'email')


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'})
    phone_number = PhoneNumberField(required=True)

    class Meta:
        model = Account
        fields = ('phone_number', 'password')


class StatusSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField(required=True)
    token = serializers.CharField(required=True)

    def validate(self, data):
        user = get_object_or_404(Account, phone_number=data['phone_number'])
        if user:
            token = Token.objects.get(user=user)
            if token.key != data['token']:
                raise ValidationError("Invalid Token")
        else:
            raise ValidationError("Invalid phone number")
        return data

    class Meta:
        model = Status
        fields = ('phone_number', 'token', 'status')
