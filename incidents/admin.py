from django.contrib import admin
from django.apps import apps

# Intentamos obtener los modelos de forma perezosa para no romper makemigrations
Incident = apps.get_model('incidents', 'Incident')
MaintenanceTask = apps.get_model('incidents', 'MaintenanceTask')

@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = ('id', 'kind', 'label', 'camera_name', 'confidence', 'created_at', 'created_by')
    list_filter = ('kind', 'camera_name', 'created_at')
    search_fields = ('label', 'camera_name', 'created_by__email')
    date_hierarchy = 'created_at'

if MaintenanceTask:  # solo registrar si existe
    @admin.register(MaintenanceTask)
    class MaintenanceTaskAdmin(admin.ModelAdmin):
        list_display = ('id', 'title', 'status', 'assigned_to', 'due_date', 'updated_at')
        list_filter = ('status', 'due_date', 'updated_at')
        search_fields = ('title', 'description', 'assigned_to__email', 'created_by__email')
        date_hierarchy = 'updated_at'
