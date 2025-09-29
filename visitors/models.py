from django.db import models
from django.conf import settings
from residents.models import Resident

class VisitorLog(models.Model):
    class Type(models.TextChoices):
        PEDESTRIAN = 'PEDESTRIAN', 'Peatón'
        VEHICLE = 'VEHICLE', 'Vehículo'

    class Status(models.TextChoices):
        IN = 'IN', 'Ingresó'
        OUT = 'OUT', 'Salida registrada'

    resident = models.ForeignKey(Resident, null=True, blank=True,
                                 on_delete=models.SET_NULL, related_name='visitor_logs')
    visitor_name = models.CharField(max_length=120)
    visitor_id = models.CharField(max_length=40, blank=True, null=True)  # CI opcional
    vehicle_plate = models.CharField(max_length=20, blank=True, null=True)
    photo_url = models.TextField(blank=True, null=True)

    kind = models.CharField(max_length=12, choices=Type.choices, default=Type.PEDESTRIAN)
    status = models.CharField(max_length=6, choices=Status.choices, default=Status.IN)

    check_in = models.DateTimeField(auto_now_add=True)
    check_out = models.DateTimeField(null=True, blank=True)

    guard = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                              null=True, related_name='guard_visits')
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-check_in']
