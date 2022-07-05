from rest_framework import serializers

from apps.tickets.models import Purchase
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    """
    Payment serializer
    """
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ('id', 'created_at')

    def validate(self, attrs):
        ticket = attrs.get('ticket')
        user = attrs.get('user')

        try:
            ticket = Purchase.objects.get(ticket=ticket, user=user, available=True)
            if ticket:
                raise serializers.ValidationError({ 'error': 'Vous avez déjà réservé ce billet'})
        except Purchase.DoesNotExist:
            return attrs
