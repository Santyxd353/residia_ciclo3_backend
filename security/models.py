from django.db import models

class Detection(models.Model):
    DETECT_TYPES = (
        ('FACE', 'Face'),
    )
    dtype = models.CharField(max_length=16, choices=DETECT_TYPES, default='FACE')
    confidence = models.FloatField(default=1.0)
    captured_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='detections/%Y/%m/%d/', null=True, blank=True)
    note = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-captured_at']

    def __str__(self):
        return f'{self.dtype} @ {self.captured_at:%Y-%m-%d %H:%M:%S}'
