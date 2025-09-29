from django.contrib import admin
from .models import CommonArea, Reservation

@admin.register(CommonArea)
class CommonAreaAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active', 'open_time', 'close_time')
    list_filter = ('is_active',)
    search_fields = ('name',)

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'area', 'resident', 'date', 'start_time', 'end_time', 'status', 'created_at')
    list_filter = ('status', 'date', 'area')
    search_fields = ('area__name', 'resident__user__email')
