from django.contrib import admin
from .models import Detection

@admin.register(Detection)
class DetectionAdmin(admin.ModelAdmin):
    list_display = ('id','dtype','captured_at')
    list_filter = ('dtype',)
    readonly_fields = ('captured_at',)
