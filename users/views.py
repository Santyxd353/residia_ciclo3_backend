from rest_framework.views import APIView
from rest_framework import permissions
from .serializers import UserLiteSerializer
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import User
from .serializers import UserLiteSerializer

class IsAdminRole(permissions.BasePermission):
    def has_permission(self, request, view):
        u = request.user
        return bool(u and (u.is_superuser or getattr(u, 'role', None) == 'ADMIN'))

class UserListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminRole]
    serializer_class = UserLiteSerializer
    queryset = User.objects.all().order_by('email')

class UserRoleUpdateView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminRole]
    serializer_class = UserLiteSerializer
    queryset = User.objects.all()

    def patch(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        new_role = request.data.get('role')
        valid = [c[0] for c in User.Role.choices] if hasattr(User, 'Role') else ['ADMIN','SECURITY','MAINTENANCE','RESIDENT']
        if new_role not in valid:
            return Response({'detail':'Rol inválido'}, status=status.HTTP_400_BAD_REQUEST)
        user.role = new_role
        # si marcas staff para ADMIN:
        user.is_staff = user.is_staff or (new_role == 'ADMIN')
        user.save()
        return Response(UserLiteSerializer(user).data)
class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        return Response(UserLiteSerializer(request.user).data)