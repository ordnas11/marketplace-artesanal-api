from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProdutoArtesanalViewSet,
    FormaVendaViewSet,
    produtos_ativos,
    produtos_usuario_logado,
    relatorio_resumo,
)

router = DefaultRouter()
router.register(r'produtos', ProdutoArtesanalViewSet, basename='produtos')
router.register(r'formas-venda', FormaVendaViewSet, basename='formas-venda')

urlpatterns = [
    path('', include(router.urls)),
    path('produtos/ativos/', produtos_ativos, name='produtos-ativos'),
    path('produtos/usuario/', produtos_usuario_logado, name='produtos-usuario'),
    path('relatorios/resumo/', relatorio_resumo, name='relatorio-resumo'),
]
