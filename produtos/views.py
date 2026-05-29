from django.db.models import Count, Sum
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import ProdutoArtesanal, FormaVenda
from .serializers import ProdutoArtesanalSerializer, FormaVendaSerializer
from .permissions import IsDonoDoObjeto


class ProdutoArtesanalViewSet(viewsets.ModelViewSet):
    serializer_class = ProdutoArtesanalSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsDonoDoObjeto]

    def get_queryset(self):
        # Usuário sem autenticação visualiza apenas produtos ativos.
        if not self.request.user.is_authenticated:
            return ProdutoArtesanal.objects.filter(status=True).order_by('-criado_em')

        # Se passar ?meus=true, lista apenas produtos do usuário logado.
        meus = self.request.query_params.get('meus')
        if meus == 'true':
            return ProdutoArtesanal.objects.filter(usuario_responsavel=self.request.user).order_by('-criado_em')

        return ProdutoArtesanal.objects.all().order_by('-criado_em')

    def perform_create(self, serializer):
        serializer.save(usuario_responsavel=self.request.user)


class FormaVendaViewSet(viewsets.ModelViewSet):
    serializer_class = FormaVendaSerializer
    permission_classes = [permissions.IsAuthenticated, IsDonoDoObjeto]

    def get_queryset(self):
        # Lista apenas formas de venda de produtos do usuário logado.
        return FormaVenda.objects.filter(produto__usuario_responsavel=self.request.user).order_by('-criado_em')

    def perform_create(self, serializer):
        produto = serializer.validated_data['produto']
        if produto.usuario_responsavel != self.request.user:
            raise PermissionError('Você só pode criar forma de venda para seus próprios produtos.')
        serializer.save()


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def produtos_ativos(request):
    produtos = ProdutoArtesanal.objects.filter(status=True).order_by('-criado_em')
    serializer = ProdutoArtesanalSerializer(produtos, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def produtos_usuario_logado(request):
    produtos = ProdutoArtesanal.objects.filter(usuario_responsavel=request.user).order_by('-criado_em')
    serializer = ProdutoArtesanalSerializer(produtos, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def relatorio_resumo(request):
    produtos_usuario = ProdutoArtesanal.objects.filter(usuario_responsavel=request.user)

    dados = {
        'usuario': request.user.username,
        'total_produtos': produtos_usuario.count(),
        'produtos_ativos': produtos_usuario.filter(status=True).count(),
        'produtos_inativos': produtos_usuario.filter(status=False).count(),
        'valor_total_cadastrado': produtos_usuario.aggregate(total=Sum('preco'))['total'] or 0,
        'formas_de_venda_cadastradas': FormaVenda.objects.filter(produto__usuario_responsavel=request.user).count(),
        'produtos_por_categoria': list(
            produtos_usuario.values('categoria').annotate(total=Count('id')).order_by('categoria')
        )
    }
    return Response(dados)
