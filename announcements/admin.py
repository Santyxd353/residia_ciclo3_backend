from django.contrib import admin
from .models import Announcement

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('id','title','audience','starts_at','ends_at','created_at','created_by')
    search_fields = ('title','body')
    list_filter = ('audience',)
