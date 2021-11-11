from apps.users.serializers import UserSerializer
from . import models
from rest_framework import serializers
import datetime

class PlaceSerialzer(serializers.ModelSerializer):
    class Meta:
        model = models.Place
        fields = '__all__'

    
    def update(self, instance, validated_data):
        instance.name =  validated_data.get('name', instance.name)
        instance.number = validated_data.get('number', instance.number)
        instance.save()
        return instance

class TicketSerializer(serializers.ModelSerializer):
    place = serializers.DictField(source='place.item')
    class Meta:
        model = models.Ticket
        fields = '__all__'


class TicketPostSerialzer(serializers.ModelSerializer):
    class Meta:
        model = models.Ticket
        fields = '__all__'

    def update(self, instance, validated_data):
        try:
            instance.place_id = validated_data.get('place', instance.place_id)
            instance.price = validated_data.get('price', instance.price)
            instance.currency = validated_data.get('currency', instance.currency)
            instance.event_date = validated_data.get('event_date', instance.event_date)
            instance.save()
        except Exception as e:
            raise serializers.ValidationError({ 'error': e.__str__() })

class PurchaseSerializer(serializers.ModelSerializer):
    ticket = serializers.DictField(source='ticket.item')
    user = UserSerializer()
    class Meta:
        model = models.Purchase
        fields = '__all__'

class PurchasePostSerialzer(serializers.ModelSerializer):
    class Meta:
        model = models.Purchase
        fields = '__all__'