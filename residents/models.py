from django.db import models
from django.conf import settings
from units.models import Unit

class Resident(models.Model):
    class ResidentType(models.TextChoices):
        OWNER = 'OWNER', 'Owner'
        TENANT = 'TENANT', 'Tenant'

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='resident_links')
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='residents')
    resident_type = models.CharField(max_length=10, choices=ResidentType.choices)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        unique_together = ('user', 'unit', 'start_date')
        ordering = ['unit__house_number', 'user__email']

    def __str__(self):
        return f"{self.user.email} → {self.unit} ({self.resident_type})"
