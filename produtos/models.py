from django.contrib.auth.models import User
from django.db import models


class ProdutoArtesanal(models.Model):
    CATEGORIAS = [
        ('bijuteria', 'Bijuteria'),
        ('decoracao', 'Decoração'),
        ('moda', 'Moda'),
        ('ceramica', 'Cerâmica'),
        ('papelaria', 'Papelaria'),
        ('outros', 'Outros'),
    ]

    nome = models.CharField(max_length=120)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.CharField(max_length=30, choices=CATEGORIAS, default='outros')
    status = models.BooleanField(default=True)
    usuario_responsavel = models.ForeignKey(User, on_delete=models.CASCADE, related_name='produtos')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome


class FormaVenda(models.Model):
    TIPOS = [
        ('unitaria', 'Unitária'),
        ('encomenda', 'Encomenda'),
        ('pacote', 'Pacote'),
    ]

    produto = models.ForeignKey(ProdutoArtesanal, on_delete=models.CASCADE, related_name='formas_venda')
    tipo = models.CharField(max_length=30, choices=TIPOS)
    condicoes_pagamento = models.CharField(max_length=200)
    prazo_producao_dias = models.PositiveIntegerField(default=0)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.tipo} - {self.produto.nome}'
