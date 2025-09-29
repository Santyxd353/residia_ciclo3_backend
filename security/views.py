import base64
import cv2
import numpy as np
from django.core.files.base import ContentFile
from rest_framework import permissions, views, response, generics
from .models import Detection
from .serializers import DetectionSerializer

# Cargamos clasificador Haar de rostros (incluido en OpenCV)
# Usamos el archivo que trae OpenCV internamente.
HAAR_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
FACE_CASCADE = cv2.CascadeClassifier(HAAR_PATH)

class DetectFaceView(views.APIView):
    """
    POST /api/security/detect/
    body: { "image": "data:image/jpeg;base64,..." }
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data_url = request.data.get('image')
        if not data_url or ';base64,' not in data_url:
            return response.Response({'detail': 'Imagen base64 requerida'}, status=400)

        b64 = data_url.split(';base64,', 1)[1]
        img_bytes = base64.b64decode(b64)
        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            return response.Response({'detail': 'No se pudo decodificar imagen'}, status=400)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = FACE_CASCADE.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))

        det_list = []
        # Si detecta, guardamos un snapshot con rectángulos
        if len(faces) > 0:
            # dibujar rectángulos (solo para evidencia)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)

            # re-encode para guardar
            ok, enc = cv2.imencode('.jpg', img)
            if ok:
                det = Detection.objects.create(dtype='FACE', confidence=1.0)  # Haar no da probas reales
                det.image.save('face.jpg', ContentFile(enc.tobytes()), save=True)
                det_list.append(det)

        ser = DetectionSerializer(det_list, many=True, context={'request': request})
        return response.Response({
            'count': len(faces),
            'detections': ser.data
        }, status=201)

class DetectionsList(generics.ListAPIView):
    """
    GET /api/security/detections/?dtype=FACE
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DetectionSerializer

    def get_queryset(self):
        qs = Detection.objects.all()
        dtype = self.request.query_params.get('dtype')
        if dtype:
            qs = qs.filter(dtype=dtype)
        return qs
