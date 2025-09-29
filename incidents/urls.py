from django.urls import path
from .views import (
    IncidentListCreate,
    MaintenanceTaskListCreate, MyMaintenanceTasks, MaintenanceTaskUpdateStatus
)

urlpatterns = [
    # Incidentes (IA demo)
    path('incidents/', IncidentListCreate.as_view(), name='incidents'),

    # Mantenimiento
    path('incidents/tasks/', MaintenanceTaskListCreate.as_view(), name='tasks'),
    path('incidents/tasks/my/', MyMaintenanceTasks.as_view(), name='my-tasks'),
    path('incidents/tasks/<int:pk>/status/', MaintenanceTaskUpdateStatus.as_view(), name='task-status'),
]
