from django.db import models
from django.conf import settings

class Incident(models.Model):
    class Kind(models.TextChoices):
        MOTION = 'MOTION', 'Movimiento'
        PERSON = 'PERSON', 'Persona detectada'
        VEHICLE = 'VEHICLE', 'Vehículo detectado'
        PLATE = 'PLATE', 'Placa detectada'

    kind = models.CharField(max_length=20, choices=Kind.choices, default=Kind.MOTION)
    camera_name = models.CharField(max_length=100, blank=True, default='Cam-1')
    label = models.CharField(max_length=100, blank=True, default='')
    confidence = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # 0..100
    image_url = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='incidents'
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'[{self.kind}] {self.label} @ {self.camera_name} ({self.created_at:%Y-%m-%d %H:%M})'


class MaintenanceTask(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pendiente'
        IN_PROGRESS = 'IN_PROGRESS', 'En progreso'
        DONE = 'DONE', 'Finalizada'

    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, default='')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='maintenance_tasks'
    )
    due_date = models.DateField(null=True, blank=True)
    photo_url = models.TextField(blank=True, null=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_tasks'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at', '-created_at']

    def __str__(self):
        who = self.assigned_to.email if self.assigned_to else 'sin asignar'
        return f'{self.title} [{self.status}] → {who}'
