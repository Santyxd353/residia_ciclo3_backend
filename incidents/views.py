from rest_framework import generics, permissions, views, response, status
from .models import Incident, MaintenanceTask
from .serializers import (
    IncidentSerializer,
    MaintenanceTaskSerializer, MaintenanceTaskCreateSerializer, MaintenanceTaskUpdateStatusSerializer
)

def is_admin_or_guard(user):
    return user.is_superuser or getattr(user, 'role', '') in ('ADMIN', 'SECURITY')

# ------ Incidents (listado simple para demo IA) ------
class IncidentListCreate(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Incident.objects.select_related('created_by').all().order_by('-created_at')
    serializer_class = IncidentSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

# ------ Maintenance ------
class MaintenanceTaskListCreate(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = MaintenanceTask.objects.select_related('assigned_to','created_by').all().order_by('-updated_at')
        # Si NO es admin, ver solo asignadas a él
        if not is_admin_or_guard(self.request.user):
            return qs.filter(assigned_to=self.request.user)
        return qs

    def get_serializer_class(self):
        return MaintenanceTaskCreateSerializer if self.request.method == 'POST' else MaintenanceTaskSerializer

    def perform_create(self, serializer):
        if not is_admin_or_guard(self.request.user):
            raise permissions.PermissionDenied('Solo administración/seguridad puede crear tareas')
        serializer.save()  # setea created_by en serializer.create()

class MyMaintenanceTasks(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MaintenanceTaskSerializer

    def get_queryset(self):
        return MaintenanceTask.objects.select_related('assigned_to','created_by').filter(
            assigned_to=self.request.user
        ).order_by('-updated_at')

class MaintenanceTaskUpdateStatus(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        obj = MaintenanceTask.objects.filter(pk=pk).first()
        if not obj:
            return response.Response({'detail': 'No encontrado'}, status=404)

        # Si no es admin, solo puede tocar si es el asignado
        if not is_admin_or_guard(request.user) and obj.assigned_to_id != request.user.id:
            return response.Response({'detail': 'Forbidden'}, status=403)

        ser = MaintenanceTaskUpdateStatusSerializer(obj, data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return response.Response(MaintenanceTaskSerializer(obj).data, status=200)
