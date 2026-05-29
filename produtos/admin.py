from django.contrib import admin
from .models import ProdutoArtesanal, FormaVenda


@admin.register(ProdutoArtesanal)
class ProdutoArtesanalAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'categoria', 'preco', 'status', 'usuario_responsavel', 'criado_em']
    list_filter = ['categoria', 'status']
    search_fields = ['nome', 'descricao']


@admin.register(FormaVenda)
class FormaVendaAdmin(admin.ModelAdmin):
    list_display = ['id', 'produto', 'tipo', 'condicoes_pagamento', 'prazo_producao_dias']
    list_filter = ['tipo']
