from rest_framework import serializers
from .models import Unit

# Referencia corta (para anidar en otros serializers)
class UnitRefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ('id', 'house_number')

# Serializer completo para el endpoint /api/units/
class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ('id', 'house_number', 'notes', 'created_at')

