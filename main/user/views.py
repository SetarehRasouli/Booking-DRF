from django.shortcuts import render
from .serializers import RegisterSerializer, ProviderCreateSerializer
from rest_framework import generics, permissions
# Create your views here.

class RegisterView(generics.CreateAPIView):
    serializer_class=RegisterSerializer
    permission_classes=[]


class BecomeProviderView(generics.CreateAPIView):
    serializer_class=ProviderCreateSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get_serializer_context(self):
        return {'request': self.request}
    