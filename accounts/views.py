from rest_framework import generics

from accounts.models import Accounts
from accounts.serializers import AccountSerializer, LoginSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token


class AccountCreateView(generics.CreateAPIView):
    model = Accounts
    serializer_class = AccountSerializer


class LoginView(APIView):
    model = Accounts
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(phone_number=str(serializer.data["phone_number"]), password=serializer.data["password"])
            login(request, user)
            token = Token.objects.get(user=user)
            return Response(data={'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response(data={'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST)
