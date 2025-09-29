from rest_framework import viewsets, permissions, filters
from .models import Unit
from .serializers import UnitSerializer

class UnitViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Unit.objects.all().order_by('house_number')
    serializer_class = UnitSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['house_number']
