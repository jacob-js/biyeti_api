from rest_framework import serializers

from apps.users.serializers import UserSerializer
from .models import Agent
from apps.events import models as event_models, serializers as event_serializers

class AgentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    event = event_serializers.EventSerializer(read_only=True)
    user_id = serializers.UUIDField(required=True, write_only=True)
    event_id = serializers.UUIDField(required=True, write_only=True)
    class Meta:
        model = Agent
        fields = '__all__'