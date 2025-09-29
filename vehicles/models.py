from django.db import models
from django.conf import settings
from units.models import Unit

class Vehicle(models.Model):
    id = models.BigAutoField(primary_key=True)
    plate = models.CharField(max_length=16, unique=True)
    make = models.CharField(max_length=50, blank=True, null=True)
    model = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=30, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vehicles')
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True, related_name='vehicles')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['plate']

    def __str__(self):
        return f"{self.plate}"
