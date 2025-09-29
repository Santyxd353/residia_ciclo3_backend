from rest_framework import serializers
from .models import VisitorLog

class VisitorLogSerializer(serializers.ModelSerializer):
    resident_email = serializers.EmailField(source='resident.user.email', read_only=True)

    class Meta:
        model = VisitorLog
        fields = (
            'id', 'resident', 'resident_email',
            'visitor_name', 'document_id', 'plate',
            'reason', 'photo_url',
            'checkin_time', 'checkout_time', 'created_at'
        )
        read_only_fields = ('checkin_time', 'checkout_time', 'created_at')


class VisitorLogCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitorLog
        fields = ('resident', 'visitor_name', 'document_id', 'plate', 'reason', 'photo_url')
