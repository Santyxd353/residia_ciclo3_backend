from django.urls import path
from .views import VisitorLogListCreate, VisitorCheckoutView

urlpatterns = [
    path('visitors/logs/', VisitorLogListCreate.as_view(), name='visitors-logs'),
    path('visitors/checkout/', VisitorCheckoutView.as_view(), name='visitors-checkout'),
]
