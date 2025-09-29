from django.contrib import admin
from .models import Unit

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('id','house_number','created_at')
    search_fields = ('house_number',)
