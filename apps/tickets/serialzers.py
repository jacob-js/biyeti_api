from . import models
from rest_framework import serializers

class PlaceSerialzer(serializers.ModelSerializer):
    class Meta:
        model = models.Place
        fields = '__all__'

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