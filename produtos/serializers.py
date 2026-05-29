from rest_framework import serializers
from .models import ProdutoArtesanal, FormaVenda


class FormaVendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormaVenda
        fields = ['id', 'produto', 'tipo', 'condicoes_pagamento', 'prazo_producao_dias', 'criado_em']
        read_only_fields = ['id', 'criado_em']


class ProdutoArtesanalSerializer(serializers.ModelSerializer):
    usuario_responsavel = serializers.StringRelatedField(read_only=True)
    formas_venda = FormaVendaSerializer(many=True, read_only=True)

    class Meta:
        model = ProdutoArtesanal
        fields = [
            'id', 'nome', 'descricao', 'preco', 'categoria', 'status',
            'usuario_responsavel', 'formas_venda', 'criado_em', 'atualizado_em'
        ]
        read_only_fields = ['id', 'usuario_responsavel', 'criado_em', 'atualizado_em']
