from rest_framework import serializers
from .models import Detection

class DetectionSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Detection
        fields = ('id', 'dtype', 'confidence', 'captured_at', 'image_url', 'note')

    def get_image_url(self, obj):
        req = self.context.get('request')
        if obj.image and req:
            return req.build_absolute_uri(obj.image.url)
        return None
