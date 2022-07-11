from rest_framework import serializers

from apps.wallets.models import TransferRequest, Wallet

class WalletSerializer(serializers.ModelSerializer):
    """
    Wallet serializer
    """
    class Meta:
        model = Wallet
        fields = '__all__'
        read_only_fields = ('id', 'created_at')

class TransferRequestSerializer(serializers.ModelSerializer):
    """
    Transfer request serializer
    """
    class Meta:
        model = TransferRequest
        fields = '__all__'

    def validate(self, attrs):
        try:
            wallet = Wallet.objects.get(id=attrs.get('wallet'))
            amount = attrs.get('amount')
            currency = attrs.get('currency')
            if amount <= 0:
                raise serializers.ValidationError({ 'amount': 'Please enter a correct amount' })
            if amount > wallet[f'{str(currency).lower()}_balance']:
                raise serializers.ValidationError({ 'amount': 'Insuficient balance' })
            return attrs
        except Wallet.DoesNotExist:
            raise serializers.ValidationError({ 'wallet': 'Invalid Wallet' }) from Wallet.DoesNotExist
        except Exception as exc:
            raise serializers.ValidationError({ 'server': 'Something went wrong !' }) from exc
