import cloudinary.uploader #pylint disable=import-error
from rest_framework.serializers import ModelSerializer, CharField
from apps.agents.models import Agent
from .models import Event, Category
from Utils.imageUploader import cloudPhoto

class EventSerializer(ModelSerializer):
    """
    Event model serializer
    """
    image = CharField(max_length=None, required=True, write_only=True)
    cover = CharField(max_length=None, required=False, read_only=True)

    class Meta: # pylint: disable=missing-class-docstring, too-few-public-methods
        model = Event
        fields = '__all__'

    def create(self, validated_data):
        image = validated_data.pop('image')
        res = cloudinary.uploader.upload(image)
        cover = res['url']
        validated_data.setdefault('cover', cover)
        event = Event(**validated_data)
        event.save()
        Agent.objects.create(user=validated_data.get('user'), event=event, role='admin') # pylint: disable=no-member
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

class CategorySerializer(ModelSerializer):
    """
    Category model serializer
    """
    class Meta: # pylint: disable=missing-class-docstring, too-few-public-methods
        model = Category
        fields = '__all__'
        