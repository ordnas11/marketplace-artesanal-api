from django.urls import path
from .views import CadastroUsuarioView

urlpatterns = [
    path('usuarios/', CadastroUsuarioView.as_view(), name='cadastro-usuario'),
]
