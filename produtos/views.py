from django.db.models import Count, Sum

from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import (
    ProdutoArtesanal,
    FormaVenda,
    Categoria
)

from .serializers import (
    ProdutoArtesanalSerializer,
    FormaVendaSerializer,
    CategoriaSerializer
)

from .permissions import IsDonoDoObjeto


class ProdutoArtesanalViewSet(viewsets.ModelViewSet):

    serializer_class = ProdutoArtesanalSerializer

    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsDonoDoObjeto
    ]

    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter
    ]

    search_fields = [
        'nome',
        'descricao'
    ]

    ordering_fields = [
        'nome',
        'preco',
        'criado_em'
    ]

    def get_queryset(self):

        queryset = ProdutoArtesanal.objects.all().order_by('-criado_em')

        categoria = self.request.query_params.get('categoria')

        if categoria:
            queryset = queryset.filter(categoria_id=categoria)

        if not self.request.user.is_authenticated:
            return queryset.filter(status=True)

        meus = self.request.query_params.get('meus')

        if meus == 'true':
            return queryset.filter(
                usuario_responsavel=self.request.user
            )

        return queryset

    def perform_create(self, serializer):

        serializer.save(
            usuario_responsavel=self.request.user
        )


class FormaVendaViewSet(viewsets.ModelViewSet):

    serializer_class = FormaVendaSerializer

    permission_classes = [
        permissions.IsAuthenticated,
        IsDonoDoObjeto
    ]

    def get_queryset(self):

        return FormaVenda.objects.filter(
            produto__usuario_responsavel=self.request.user
        ).order_by('-criado_em')

    def perform_create(self, serializer):

        produto = serializer.validated_data['produto']

        if produto.usuario_responsavel != self.request.user:
            raise PermissionError(
                'Você só pode criar formas de venda para seus próprios produtos.'
            )

        serializer.save()


class CategoriaViewSet(viewsets.ModelViewSet):

    queryset = Categoria.objects.all().order_by('nome')

    serializer_class = CategoriaSerializer

    permission_classes = [
        permissions.AllowAny
    ]


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def produtos_ativos(request):

    produtos = ProdutoArtesanal.objects.filter(
        status=True
    ).order_by('-criado_em')

    serializer = ProdutoArtesanalSerializer(
        produtos,
        many=True
    )

    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def produtos_usuario_logado(request):

    produtos = ProdutoArtesanal.objects.filter(
        usuario_responsavel=request.user
    ).order_by('-criado_em')

    serializer = ProdutoArtesanalSerializer(
        produtos,
        many=True
    )

    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def relatorio_resumo(request):

    produtos_usuario = ProdutoArtesanal.objects.filter(
        usuario_responsavel=request.user
    )

    dados = {

        'usuario': request.user.username,

        'total_produtos':
            produtos_usuario.count(),

        'produtos_ativos':
            produtos_usuario.filter(
                status=True
            ).count(),

        'produtos_inativos':
            produtos_usuario.filter(
                status=False
            ).count(),

        'valor_total_cadastrado':
            produtos_usuario.aggregate(
                total=Sum('preco')
            )['total'] or 0,

        'formas_de_venda_cadastradas':
            FormaVenda.objects.filter(
                produto__usuario_responsavel=request.user
            ).count(),

        'produtos_por_categoria':
            list(
                produtos_usuario
                .values('categoria__nome')
                .annotate(total=Count('id'))
                .order_by('categoria__nome')
            )
    }

    return Response(dados)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def relatorio(request):

    total = ProdutoArtesanal.objects.count()

    ativos = ProdutoArtesanal.objects.filter(
        status=True
    ).count()

    inativos = ProdutoArtesanal.objects.filter(
        status=False
    ).count()

    valor_total = ProdutoArtesanal.objects.aggregate(
        total=Sum('preco')
    )['total'] or 0

    categorias = list(
        Categoria.objects.annotate(
            quantidade=Count('produtos')
        ).values(
            'nome',
            'quantidade'
        )
    )

    return Response({

        "total_produtos": total,

        "ativos": ativos,

        "inativos": inativos,

        "valor_total_produtos": valor_total,

        "categorias": categorias
    })