from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ProdutoArtesanalViewSet,
    FormaVendaViewSet,
    CategoriaViewSet,
    produtos_ativos,
    produtos_usuario_logado,
    relatorio_resumo,
    relatorio
)

router = DefaultRouter()

router.register(
    r'produtos',
    ProdutoArtesanalViewSet,
    basename='produtos'
)

router.register(
    r'formas-venda',
    FormaVendaViewSet,
    basename='formas-venda'
)

router.register(
    r'categorias',
    CategoriaViewSet,
    basename='categorias'
)

urlpatterns = [

    # ViewSets
    path('', include(router.urls)),

    # Produtos públicos
    path(
        'produtos/ativos/',
        produtos_ativos,
        name='produtos-ativos'
    ),

    # Produtos do usuário logado
    path(
        'produtos/usuario/',
        produtos_usuario_logado,
        name='produtos-usuario'
    ),

    # Relatório do usuário logado
    path(
        'relatorios/resumo/',
        relatorio_resumo,
        name='relatorio-resumo'
    ),

    # Relatório geral
    path(
        'relatorios/',
        relatorio,
        name='relatorio-geral'
    ),
]