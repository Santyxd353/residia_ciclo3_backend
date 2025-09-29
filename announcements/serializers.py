from rest_framework import serializers
from .models import Announcement

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ('id','title','body','audience','starts_at','ends_at','created_at','created_by')
        read_only_fields = ('id','created_at','created_by')
