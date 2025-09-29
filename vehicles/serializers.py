from rest_framework import serializers
from .models import Vehicle

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ('id','plate','make','model','color','user','unit','created_at')
        read_only_fields = ('id','created_at')
