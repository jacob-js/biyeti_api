from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    """
    Payment serializer
    """
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ('id', 'created_at')

class PaymentRequestSerializer(serializers.Serializer): # pylint: disable=abstract-method
    """
    Payment request serializer
    """
    phone = serializers.CharField(max_length=255)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField(max_length=3)
