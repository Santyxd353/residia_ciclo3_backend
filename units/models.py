from django.db import models

class Unit(models.Model):
    id = models.BigAutoField(primary_key=True)
    house_number = models.CharField(max_length=40, unique=True, null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['house_number']

    def __str__(self):
        return self.house_number
