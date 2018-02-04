from rest_framework import generics

from accounts.models import Accounts
from accounts.serializers import AccountSerializer

class AccountCreateView(generics.CreateAPIView):
    model = Accounts
    serializer_class = AccountSerializer
