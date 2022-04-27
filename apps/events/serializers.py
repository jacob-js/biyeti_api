from venv import create
from rest_framework import serializers;
from .models import Event, Category
from apps.agents.models import Agent;
import cloudinary.uploader;

class EventSerializer(serializers.ModelSerializer):
    image = serializers.CharField(max_length=None, required=True, write_only=True)
    cover = serializers.CharField(max_length=None, required=False, read_only=True)
    class Meta:
        model = Event
        fields = '__all__'
        
    def create(self, validated_data):
        image = validated_data.pop('image')
        res = cloudinary.uploader.upload(image)
        cover = res['url']
        validated_data.setdefault('cover', cover)
        event = Event(**validated_data)
        event.save()
        Agent.objects.create(user=validated_data.get('user'), event=event, role='admin')
        return event

    def update(self, instance, validated_data: dict):
        try:
            image = validated_data.pop('image')
            if image != instance.cover:
                res = cloudinary.uploader.upload(image)
                cover = res['url']
                validated_data.setdefault('cover', cover)
        except KeyError:
            pass

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'