from accounts.models import Account, Status
from accounts.serializers import AccountSerializer, LoginSerializer, StatusSerializer

from django.contrib.auth import authenticate, login

from rest_framework import generics
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class AccountCreateView(generics.CreateAPIView):
    model = Account
    serializer_class = AccountSerializer

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()


class LoginView(APIView):
    model = Account
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


class StatusCreateView(generics.CreateAPIView):
    model = Status
    serializer_class = StatusSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        if serializer.is_valid():
            Status.objects.create(user=Account.objects.get(
                phone_number=serializer.validated_data['phone_number']),
                status=serializer.validated_data["status"]
            )
