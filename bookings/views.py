from rest_framework import generics, permissions, views, response
from .models import CommonArea, Reservation
from .serializers import (
    CommonAreaSerializer,
    AvailabilitySerializer,
    ReservationCreateSerializer,
    ReservationSerializer,
    ReservationListSerializer,   
)
from residents.models import Resident

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser or getattr(request.user, 'role', '') == 'ADMIN'

class AreasList(generics.ListCreateAPIView):
    queryset = CommonArea.objects.all()
    serializer_class = CommonAreaSerializer

    def get_permissions(self):
        # GET: cualquiera autenticado; POST: solo admin
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsAdmin()]
        return [permissions.IsAuthenticated()]

class AvailabilityView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, area_id):
        # Ejemplo sencillo de slots fijos (puedes reemplazar con tu lógica)
        date_str = request.query_params.get('date')
        if not date_str:
            return response.Response({'detail': 'Falta ?date=YYYY-MM-DD'}, status=400)

        # slots demo
        slots = [
            {'start': '08:00', 'end': '10:00', 'available': True},
            {'start': '10:00', 'end': '12:00', 'available': True},
            {'start': '15:00', 'end': '17:00', 'available': True},
        ]
        data = {'date': date_str, 'area_id': area_id, 'slots': slots}
        ser = AvailabilitySerializer(data=data)
        ser.is_valid(raise_exception=False)  # opcional
        return response.Response(ser.data)

class ReserveView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        ser = ReservationCreateSerializer(data=request.data, context={'request': request})
        ser.is_valid(raise_exception=True)
        obj = ser.save()
        return response.Response(ReservationSerializer(obj).data, status=201)

class MyReservationsView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReservationSerializer

    def get_queryset(self):
        user = self.request.user
        # si hay Resident relacionado, filtra por él
        res = Resident.objects.filter(user=user).first()
        if res:
            return Reservation.objects.filter(resident=res).order_by('-date', '-start_time')
        # admin podría listar todas sus reservas (vacío si no es residente)
        return Reservation.objects.none()
def get_my_resident(user):
    """Admin/Superuser -> None (ve todo); Residente -> su objeto Resident."""
    if user.is_superuser or getattr(user, 'role', '') == 'ADMIN':
        return None
    return Resident.objects.filter(user=user).select_related('unit','user').first()

class ReservationsListView(generics.ListAPIView):
    """
    GET /api/bookings/reservations/
      - Admin: ve todas (puede filtrar con ?area_id=&date=YYYY-MM-DD)
      - Residente: ve solo sus reservas
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReservationListSerializer

    def get_queryset(self):
        qs = Reservation.objects.select_related(
            'area', 'resident', 'resident__user', 'resident__unit'
        ).order_by('-date', '-start_time', '-created_at')

        area_id = self.request.query_params.get('area_id')
        date_str = self.request.query_params.get('date')
        if area_id:
            qs = qs.filter(area_id=area_id)
        if date_str:
            qs = qs.filter(date=date_str)

        me_res = get_my_resident(self.request.user)
        if me_res:
            qs = qs.filter(resident=me_res)
        return qs