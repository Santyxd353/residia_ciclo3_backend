from django.utils.timezone import now
from django.db.models import Q           # <-- agrega esto
from rest_framework import viewsets, filters, permissions
from .models import Announcement
from .serializers import AnnouncementSerializer
from .permissions import IsAdminOrReadOnly

class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title','body']

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.method in ('GET',):
            now_ts = now()
            qs = qs.filter(
                Q(starts_at__isnull=True) | Q(starts_at__lte=now_ts),
                Q(ends_at__isnull=True) | Q(ends_at__gte=now_ts),
            )
        return qs

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
