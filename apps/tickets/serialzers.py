from apps.users.serializers import UserSerializer
from . import models
from rest_framework import serializers

class EventSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = models.Event
        fields = '__all__'

class EventPostSerialzer(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        fields = '__all__'

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ticket
        fields = '__all__'


class TicketPostSerialzer(serializers.ModelSerializer):
    class Meta:
        model = models.Ticket
        fields = '__all__'

    def update(self, instance, validated_data):
        try:
            instance.name = validated_data.get('name', instance.name)
            instance.price = validated_data.get('price', instance.price)
            instance.currency = validated_data.get('currency', instance.currency)
            instance.event_date = validated_data.get('event_date', instance.event_date)
            instance.save()
        except Exception as exception:
            raise serializers.ValidationError({ 'error': exception.__str__() })

class PurchaseSerializer(serializers.ModelSerializer):
    """
    Purchase serializer
    """
    ticket = TicketSerializer()
    user = UserSerializer()
    class Meta:
        model = models.Purchase
        fields = '__all__'

class PurchasePostSerialzer(serializers.ModelSerializer):
    class Meta:
        model = models.Purchase
        fields = '__all__'

    def validate(self, attrs):
        ticket = attrs.get('ticket')
        user = attrs.get('user')
        interval = attrs.get('interval')

        try:
            ticket = models.Purchase.objects.get(ticket=ticket, user=user, interval=interval, available=True)
            if ticket:
                raise serializers.ValidationError({ 'error': 'Vous avez déjà réservé ce billet'})
        except models.Purchase.DoesNotExist:
            return attrs