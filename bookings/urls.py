# bookings/urls.py
from django.urls import path
from .views import AreasList, AvailabilityView, ReserveView, MyReservationsView, ReservationsListView  # ← AGREGA

urlpatterns = [
    path('bookings/areas/', AreasList.as_view(), name='areas-list'),
    path('bookings/availability/<int:area_id>/', AvailabilityView.as_view(), name='availability'),
    path('bookings/reserve/', ReserveView.as_view(), name='reserve'),
    path('bookings/my/', MyReservationsView.as_view(), name='my-reservations'),
    path('bookings/reservations/', ReservationsListView.as_view(), name='reservations-list'),  # ← NUEVA
]
