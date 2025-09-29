from django.contrib import admin
from .models import VisitorLog

@admin.register(VisitorLog)
class VisitorLogAdmin(admin.ModelAdmin):
    list_display = ('id','visitor_name','vehicle_plate','resident','status','check_in','check_out','guard')
    list_filter = ('status','kind','check_in')
    search_fields = ('visitor_name','vehicle_plate','visitor_id')
