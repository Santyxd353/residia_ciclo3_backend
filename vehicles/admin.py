from django.contrib import admin
from .models import Vehicle

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('id','plate','make','model','color','user','unit','created_at')
    search_fields = ('plate','user__email','unit__block','unit__number')
