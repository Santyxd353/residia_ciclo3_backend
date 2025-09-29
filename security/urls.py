from django.urls import path
from .views import DetectFaceView, DetectionsList

urlpatterns = [
    path('security/detect/', DetectFaceView.as_view(), name='security-detect'),
    path('security/detections/', DetectionsList.as_view(), name='security-detections'),
]
