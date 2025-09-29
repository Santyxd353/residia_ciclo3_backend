from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ResidentViewSet, ResidentRegisterView

router = DefaultRouter()
router.register(r'residents', ResidentViewSet, basename='resident')

urlpatterns = [
    path('residents/register', ResidentRegisterView.as_view(), name='resident-register'),
]

urlpatterns += router.urls
