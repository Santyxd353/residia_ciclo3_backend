from rest_framework import generics, permissions, views, response, status
from django.db.models import Q
from residents.models import Resident
from .models import VisitorLog
from .serializers import VisitorLogSerializer, VisitorLogCreateSerializer

def is_admin_or_guard(user):
    return user.is_superuser or getattr(user, 'role', '') in ('ADMIN', 'SECURITY')

class VisitorLogListCreate(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = VisitorLog.objects.select_related('resident__user').all()

    def get_serializer_class(self):
        return VisitorLogCreateSerializer if self.request.method == 'POST' else VisitorLogSerializer

    def get_queryset(self):
        qs = super().get_queryset()

        # Filtros (opcional): ?from=YYYY-MM-DD&to=YYYY-MM-DD&email=...
        dfrom = self.request.query_params.get('from')
        dto   = self.request.query_params.get('to')
        email = self.request.query_params.get('email')

        if dfrom:
            qs = qs.filter(checkin_time__date__gte=dfrom)
        if dto:
            qs = qs.filter(checkin_time__date__lte=dto)
        if email:
            qs = qs.filter(resident__user__email__icontains=email)

        # Si NO es admin/guard, mostrar solo lo del residente dueño
        if not is_admin_or_guard(self.request.user):
            res = Resident.objects.filter(user=self.request.user).first()
            if res:
                qs = qs.filter(resident=res)
            else:
                qs = qs.none()

        return qs.order_by('-checkin_time', '-id')

    def perform_create(self, serializer):
        # Solo admin/guard pueden registrar entradas
        if not is_admin_or_guard(self.request.user):
            raise permissions.PermissionDenied('Solo seguridad/administración')
        serializer.save()  # checkin_time lo pone auto_now_add en el modelo


class VisitorCheckoutView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # Solo admin/guard pueden dar salida
        if not is_admin_or_guard(request.user):
            return response.Response({'detail':'Forbidden'}, status=403)

        log_id = request.data.get('id')
        obj = VisitorLog.objects.filter(id=log_id).first()
        if not obj:
            return response.Response({'detail':'Log no encontrado'}, status=404)

        if obj.checkout_time:
            return response.Response({'detail':'Ya tenía checkout'}, status=400)

        from django.utils.timezone import now
        obj.checkout_time = now()
        obj.save(update_fields=['checkout_time'])
        return response.Response(VisitorLogSerializer(obj).data, status=200)
