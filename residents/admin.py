from django.contrib import admin
from .models import Resident

@admin.register(Resident)
class ResidentAdmin(admin.ModelAdmin):
    list_display = ('id','user','unit','resident_type','start_date','end_date')
    list_filter = ('resident_type',)
    search_fields = ('user__email','unit__block','unit__number')
