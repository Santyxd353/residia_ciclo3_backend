from django.db import models
from django.conf import settings

class Announcement(models.Model):
    class Audience(models.TextChoices):
        ALL = 'ALL', 'Todos'
        RESIDENTS = 'RESIDENTS', 'Residentes'
        STAFF = 'STAFF', 'Personal'

    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=160)
    body = models.TextField()
    audience = models.CharField(max_length=16, choices=Audience.choices, default=Audience.ALL)
    starts_at = models.DateTimeField(null=True, blank=True)
    ends_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='announcements_created')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
