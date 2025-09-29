from django.db import IntegrityError, transaction
from rest_framework import serializers
from .models import Resident
from users.models import User
from units.models import Unit

# Si ya tienes estos serializers en sus apps, se importan.
# UnitRefSerializer debe existir en units/serializers.py
try:
    from units.serializers import UnitRefSerializer
except Exception:
    # Fallback mínimo por si no existe
    class UnitRefSerializer(serializers.ModelSerializer):
        class Meta:
            model = Unit
            fields = ("id", "house_number")

# UserBasicSerializer debe existir en users/serializers.py
try:
    from users.serializers import UserBasicSerializer
except Exception:
    class UserBasicSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = (
                "id",
                "email",
                "first_name",
                "last_name",
                "national_id",
                "phone",
                "photo_url",
            )

class ResidentSerializer(serializers.ModelSerializer):
    user_detail = UserBasicSerializer(source="user", read_only=True)
    unit_detail = UnitRefSerializer(source="unit", read_only=True)

    class Meta:
        model = Resident
        fields = (
            "id",
            "resident_type",
            "start_date",
            "user",          # id
            "unit",          # id
            "user_detail",   # expandido
            "unit_detail",   # expandido
        )
        read_only_fields = ("start_date",)

# --- Registro completo (crea User + Unit (si no existe) + Resident) ---

class NestedUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField(allow_blank=True, required=False)
    last_name = serializers.CharField(allow_blank=True, required=False)
    national_id = serializers.CharField(allow_blank=True, required=False)
    phone = serializers.CharField(allow_blank=True, required=False)
    photo_url = serializers.CharField(allow_blank=True, required=False)
    # opcional: si lo envías, se setea; si no, queda una default
    password = serializers.CharField(write_only=True, required=False, allow_blank=True, min_length=4)

class ResidentRegisterSerializer(serializers.Serializer):
    resident_type = serializers.ChoiceField(choices=[("OWNER","OWNER"), ("TENANT","TENANT")], default="OWNER")
    house_number = serializers.CharField()
    user = NestedUserSerializer()
    # vehículos opcional; si tienes app vehicles se crean, si no se ignora
    vehicles = serializers.ListField(child=serializers.DictField(), required=False)

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        vehicles_data = validated_data.pop("vehicles", [])

        email = user_data.get("email").lower().strip()
        password = user_data.get("password") or "12345678"  # default simple (puedes cambiarla en admin)
        username = email.split("@")[0]  # username interno

        with transaction.atomic():
            # User
            if User.objects.filter(email=email).exists():
                raise serializers.ValidationError({"user": {"email": "Ya existe un usuario con este email."}})
            if user_data.get("national_id"):
                if User.objects.filter(national_id=user_data["national_id"]).exists():
                    raise serializers.ValidationError({"user": {"national_id": "Ya existe usuario con este CI."}})

            u = User(
                email=email,
                username=username,
                first_name=user_data.get("first_name", ""),
                last_name=user_data.get("last_name", ""),
                national_id=user_data.get("national_id") or None,
                phone=user_data.get("phone", ""),
                photo_url=user_data.get("photo_url", ""),
                role="RESIDENT",
                status="ACTIVE",
                is_active=True,
            )
            u.set_password(password)
            u.save()

            # Unit
            house_number = validated_data["house_number"].strip()
            unit, _ = Unit.objects.get_or_create(house_number=house_number)

            # Resident
            resident = Resident.objects.create(
                user=u,
                unit=unit,
                resident_type=validated_data.get("resident_type", "OWNER"),
            )

            # Vehicles (opcional)
            try:
                from vehicles.models import Vehicle
                for v in vehicles_data or []:
                    plate = (v.get("plate") or "").strip()
                    if not plate:
                        continue
                    Vehicle.objects.get_or_create(
                        resident=resident,
                        plate=plate,
                        defaults={
                            "make": v.get("make", ""),
                            "model": v.get("model", ""),
                            "color": v.get("color", ""),
                        },
                    )
            except Exception:
                # si no existe el app vehicles o falla, no rompemos el registro
                pass

        return resident

    def to_representation(self, instance):
        # al terminar, devolvemos el residente expandido
        return ResidentSerializer(instance).data
