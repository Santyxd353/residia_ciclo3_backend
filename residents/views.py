from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework import viewsets, filters, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Resident
from .serializers import ResidentSerializer, ResidentRegisterSerializer
from .permissions import IsAdminOrReadOnly
from units.models import Unit
from users.models import User

class ResidentViewSet(viewsets.ModelViewSet):
    queryset = Resident.objects.select_related('user', 'unit').all().order_by('id')
    serializer_class = ResidentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    # Ajustado a tu modelo actual (house_number + datos de usuario)
    search_fields = [
        'user__email', 'user__first_name', 'user__last_name',
        'user__national_id', 'user__phone',
        'unit__house_number', 'resident_type'
    ]

    @transaction.atomic
    def partial_update(self, request, *args, **kwargs):
        """
        PATCH /api/residents/<id>/
        Permite actualizar:
          - resident_type
          - house_number (crea/relaciona Unit por número de casa)
          - datos del usuario (email, first_name, last_name, national_id, phone, photo_url)
        Solo ADMIN o superuser.
        """
        user = request.user
        if not (user.is_superuser or getattr(user, 'role', None) == 'ADMIN'):
            return Response({'detail': 'Forbidden'}, status=403)

        resident = self.get_object()
        data = request.data or {}

        # update resident_type
        if 'resident_type' in data:
            resident.resident_type = data['resident_type']

        # update house_number -> Unit
        house_number = data.get('house_number')
        if house_number:
            unit, _ = Unit.objects.get_or_create(house_number=house_number)
            resident.unit = unit

        # update user fields (nested)
        u = data.get('user') or {}
        changed = False
        for f in ['first_name', 'last_name', 'national_id', 'phone', 'photo_url', 'email']:
            if f in u:
                setattr(resident.user, f, u[f])
                changed = True
        if changed:
            # si quieres sincronizar username cuando no existe
            if 'email' in u and not resident.user.username:
                resident.user.username = u['email'].split('@')[0]
            resident.user.save()

        resident.save()
        return Response(ResidentSerializer(resident).data, status=200)


class ResidentRegisterView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # Solo ADMIN / superuser puede registrar residentes
        if request.user.role != 'ADMIN' and not request.user.is_superuser:
            return Response({'detail': 'Forbidden'}, status=403)

        ser = ResidentRegisterSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        instance = ser.save()  # el serializer ya hace user.set_password, role=RESIDENT, is_active=True
        return Response(ser.to_representation(instance), status=201)
