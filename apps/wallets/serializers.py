from rest_framework import serializers

from apps.wallets.models import Wallet

class WalletSerializer(serializers.ModelSerializer):
    """
    Wallet serializer
    """
    class Meta:
        model = Wallet
        fields = '__all__'
        read_only_fields = ('id', 'created_at')
        