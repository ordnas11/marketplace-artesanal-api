from django.contrib.auth.models import User
from django.db import models


class Categoria(models.Model):

    nome = models.CharField(
        max_length=100,
        unique=True
    )

    descricao = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return self.nome


class ProdutoArtesanal(models.Model):

    nome = models.CharField(max_length=120)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='produtos'
    )

    status = models.BooleanField(default=True)

    usuario_responsavel = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='produtos'
    )

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome


class FormaVenda(models.Model):

    TIPOS = [
        ('unitaria', 'Unitária'),
        ('encomenda', 'Encomenda'),
        ('pacote', 'Pacote'),
        ('assinatura', 'Assinatura'),
    ]

    produto = models.ForeignKey(
        ProdutoArtesanal,
        on_delete=models.CASCADE,
        related_name='formas_venda'
    )

    tipo = models.CharField(max_length=30, choices=TIPOS)

    condicoes_pagamento = models.CharField(max_length=200)

    prazo_producao_dias = models.PositiveIntegerField(default=0)

    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.tipo} - {self.produto.nome}'


class Favorito(models.Model):

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    produto = models.ForeignKey(
        ProdutoArtesanal,
        on_delete=models.CASCADE
    )

    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'produto')

    def __str__(self):
        return f'{self.usuario.username} - {self.produto.nome}'


class Avaliacao(models.Model):

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    produto = models.ForeignKey(
        ProdutoArtesanal,
        on_delete=models.CASCADE
    )

    nota = models.IntegerField()

    comentario = models.TextField()

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f'{self.produto.nome} - Nota {self.nota}'
