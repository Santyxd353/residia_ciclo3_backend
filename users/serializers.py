from rest_framework import serializers
from .models import User

class UserLiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'national_id',
            'phone',
            'photo_url',
            'role',
            'is_superuser',
            'is_active',
        )
        read_only_fields = ('id', 'is_superuser', 'is_active')

# Alias por compatibilidad si en algún lugar importan UserBasicSerializer
class UserBasicSerializer(UserLiteSerializer):
    pass
