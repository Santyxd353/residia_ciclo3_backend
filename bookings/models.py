from django.db import models
from residents.models import Resident

class CommonArea(models.Model):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    # opcionales: horarios de referencia
    open_time = models.TimeField(null=True, blank=True)
    close_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class Reservation(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pendiente'
        APPROVED = 'APPROVED', 'Aprobada'
        CANCELED = 'CANCELED', 'Cancelada'

    area = models.ForeignKey(CommonArea, on_delete=models.CASCADE, related_name='reservations')
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE, related_name='reservations')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.PENDING)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-start_time']
        # Evitar duplicados exactos
        unique_together = ('area', 'date', 'start_time', 'end_time')

    def __str__(self):
        return f'{self.area.name} {self.date} {self.start_time}-{self.end_time}'
