from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Solo ADMIN puede crear/editar/eliminar. Otros roles solo lectura (si expones GET públicos).
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_authenticated and request.user.role == 'ADMIN'
