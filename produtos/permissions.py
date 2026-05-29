from rest_framework import permissions


class IsDonoDoObjeto(permissions.BasePermission):
    """Permite alteração apenas para o usuário responsável pelo produto."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if hasattr(obj, 'usuario_responsavel'):
            return obj.usuario_responsavel == request.user
        if hasattr(obj, 'produto'):
            return obj.produto.usuario_responsavel == request.user
        return False
