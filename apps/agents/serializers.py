import email
from rest_framework import serializers
from django.db.models import Q

from apps.users.serializers import UserSerializer
from .models import Agent
from apps.users.models import User
from apps.events.models import Event
from apps.events import models as event_models, serializers as event_serializers

class AgentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    event = event_serializers.EventSerializer(read_only=True)
    role = serializers.CharField(required=True)
    user_id = serializers.CharField(required=True, write_only=True)
    event_id = serializers.UUIDField(required=True, write_only=True)
    class Meta:
        model = Agent
        fields = '__all__'

    def create(self, validated_data: dict):
        user_id = validated_data.__getitem__('user_id')
        event_id = validated_data.__getitem__('event_id')
        role = validated_data.__getitem__('role')
        try:
            user = User.objects.get(Q(email=user_id) | Q(phone_number=user_id))
        except User.DoesNotExist:
            raise serializers.ValidationError({ 'user_id': "Utilisateur incorrect" }, 404)
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            raise serializers.ValidationError({ 'event_id': "Evenement introuvable" }, 404)
        try:
            agent = Agent.objects.get(user=user.id, event=event.id)
            if agent:
                raise serializers.ValidationError({ "agent": "L'agent existe déjà" })
        except Agent.DoesNotExist:
            agent = Agent.objects.create(user=user, event=event, role=role)
            
        return agent
        

    def update(self, instance, validated_data):
        instance.role = validated_data.get('role', instance.role)
        instance.save()
        return instance