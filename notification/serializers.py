from rest_framework import serializers
from .models import Notification
from authentication.serializers import UserSerializer

class NotificationCreateSerializer(serializers.ModelSerializer):
    is_read = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Notification
        fields = ('message', 'is_read', 'user')

class NotificationListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    source_user = UserSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ('message', 'user', 'source_user','is_read')