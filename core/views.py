from django.contrib.auth.models import User
from rest_framework import generics, permissions
from .serializers import UsuarioSerializer


class CadastroUsuarioView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.AllowAny]
