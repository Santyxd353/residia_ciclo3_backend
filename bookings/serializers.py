# bookings/serializers.py
from datetime import datetime, time
from rest_framework import serializers
from .models import CommonArea, Reservation
from residents.models import Resident

# ----- ÁREAS COMUNES -----

class CommonAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommonArea
        # Solo los campos que EXISTEN en tu modelo
        fields = ('id', 'name', 'description', 'is_active')

# ----- DISPONIBILIDAD (simple) -----
# Lo usamos para estructurar la respuesta de availability (si la quieres como serializer).
# Si devuelves un array crudo en la vista, no es estrictamente necesario, pero no estorba.
class AvailabilitySlotSerializer(serializers.Serializer):
    start = serializers.CharField()
    end = serializers.CharField()
    available = serializers.BooleanField()

class AvailabilitySerializer(serializers.Serializer):
    date = serializers.DateField()
    area_id = serializers.IntegerField()
    slots = AvailabilitySlotSerializer(many=True)


# ----- RESERVAS -----
class ReservationSerializer(serializers.ModelSerializer):
    area_detail = CommonAreaSerializer(source='area', read_only=True)

    class Meta:
        model = Reservation
        fields = (
            'id', 'area', 'area_detail',
            'resident', 'date', 'start_time', 'end_time',
            'created_at'
        )
        read_only_fields = ('resident', 'created_at')

class ReservationCreateSerializer(serializers.ModelSerializer):
    area_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Reservation
        fields = ('area_id', 'date', 'start_time', 'end_time')

    def validate(self, attrs):
        request = self.context.get('request')
        if not request or not request.user or not request.user.is_authenticated:
            raise serializers.ValidationError('No autenticado')

        # traer Resident del usuario actual
        res = Resident.objects.filter(user=request.user).first()
        if not res:
            raise serializers.ValidationError('El usuario no tiene perfil de residente')

        # Normalizar datos
        try:
            # asegurar tipos correctos
            date_val = attrs.get('date')
            if isinstance(date_val, str):
                date_val = datetime.strptime(date_val, '%Y-%m-%d').date()

            st_val = attrs.get('start_time')
            if isinstance(st_val, str):
                st_val = datetime.strptime(st_val, '%H:%M').time()

            en_val = attrs.get('end_time')
            if isinstance(en_val, str):
                en_val = datetime.strptime(en_val, '%H:%M').time()
        except Exception:
            raise serializers.ValidationError('Formato de fecha/hora inválido')

        if en_val <= st_val:
            raise serializers.ValidationError('La hora de fin debe ser mayor a la de inicio')

        # verificar solapamientos
        area_id = attrs.get('area_id')
        qs = Reservation.objects.filter(area_id=area_id, date=date_val)
        overlap = qs.filter(start_time__lt=en_val, end_time__gt=st_val).exists()
        if overlap:
            raise serializers.ValidationError('Ya existe una reserva que se solapa en ese horario')

        # guardar objetos útiles en validated_data
        attrs['resident_obj'] = res
        attrs['date'] = date_val
        attrs['start_time'] = st_val
        attrs['end_time'] = en_val
        return attrs

    def create(self, validated_data):
        res = validated_data.pop('resident_obj')
        area_id = validated_data.pop('area_id')
        return Reservation.objects.create(
            area_id=area_id,
            resident=res,
            **validated_data
        )
# --- al final de bookings/serializers.py ---

class ReservationListSerializer(serializers.ModelSerializer):
    area_detail = CommonAreaSerializer(source='area', read_only=True)
    # quién reservó (nombre/apellido/email) y casa
    who = serializers.SerializerMethodField()
    unit = serializers.SerializerMethodField()

    class Meta:
        model = Reservation
        fields = (
            'id', 'date', 'start_time', 'end_time',
            'area', 'area_detail',
            'who', 'unit',
            'created_at',
        )

    def get_who(self, obj):
        u = getattr(obj.resident, 'user', None)
        if not u:
            return None
        return {
            'email': getattr(u, 'email', None),
            'first_name': getattr(u, 'first_name', ''),
            'last_name': getattr(u, 'last_name', ''),
        }

    def get_unit(self, obj):
        unit = getattr(obj.resident, 'unit', None)
        return getattr(unit, 'house_number', None)
