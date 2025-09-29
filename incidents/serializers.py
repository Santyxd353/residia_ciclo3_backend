from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Incident, MaintenanceTask

User = get_user_model()

# Incidentes (ya con IA simple)
class IncidentSerializer(serializers.ModelSerializer):
    created_by_email = serializers.EmailField(source='created_by.email', read_only=True)

    class Meta:
        model = Incident
        fields = ('id','kind','camera_name','label','confidence','image_url','created_at','created_by','created_by_email')
        read_only_fields = ('created_at',)

# Mantenimiento
class MaintenanceTaskSerializer(serializers.ModelSerializer):
    assigned_to_email = serializers.EmailField(source='assigned_to.email', read_only=True)
    created_by_email = serializers.EmailField(source='created_by.email', read_only=True)

    class Meta:
        model = MaintenanceTask
        fields = (
            'id','title','description','status','assigned_to','assigned_to_email',
            'due_date','photo_url','created_by','created_by_email','created_at','updated_at'
        )
        read_only_fields = ('created_at','updated_at','created_by')

class MaintenanceTaskCreateSerializer(serializers.ModelSerializer):
    assigned_email = serializers.EmailField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = MaintenanceTask
        fields = ('title','description','due_date','photo_url','assigned_email')

    def create(self, validated_data):
        request = self.context.get('request')
        email = validated_data.pop('assigned_email', '').strip()
        assigned = User.objects.filter(email=email).first() if email else None
        return MaintenanceTask.objects.create(
            created_by=request.user,
            assigned_to=assigned,
            **validated_data
        )

class MaintenanceTaskUpdateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceTask
        fields = ('status','photo_url','description')
