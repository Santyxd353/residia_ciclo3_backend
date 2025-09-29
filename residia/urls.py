from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/', include('units.urls')),
    path('api/', include('residents.urls')),
    path('api/', include('vehicles.urls')),
    path('api/', include('announcements.urls')),
    path('api/', include('finance.urls')),
    path('api/', include('bookings.urls')),  # ← ESTA LÍNEA DEBE EXISTIR
    path('api/', include('visitors.urls')),
    path('api/', include('incidents.urls')),
    path('api/', include('security.urls')),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)