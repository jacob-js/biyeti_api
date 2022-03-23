from venv import create
from rest_framework import serializers;
from .models import Event, Category
import cloudinary.uploader;

class EventSerializer(serializers.ModelSerializer):
    # image = serializers.ImageField(max_length=None, use_url=True, allow_empty_file=True, required=True, write_only=True)
    # cover = serializers.CharField(max_length=None, required=False, read_only=True)
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
        return event