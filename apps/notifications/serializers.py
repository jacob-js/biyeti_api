from pyexpat import model
from rest_framework import serializers

from apps.notifications.models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'