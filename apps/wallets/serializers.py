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
    phone_number = serializers.CharField(required=True)
    amount = serializers.DecimalField(required=True, max_digits=10, decimal_places=2)
    currency = serializers.CharField(required=True)

    class Meta:
        model = TransferRequest
        fields = '__all__'

    def validate(self, attrs):
        try:
            wallet = attrs.get('wallet')
            wallet = WalletSerializer(wallet).data
            amount = attrs.get('amount')
            currency = attrs.get('currency')
            if amount <= 0:
                raise serializers.ValidationError({ 'amount': 'Veuillez entrer un montant valid' })
            if amount > float(wallet[f'{str(currency).lower()}_balance']):
                raise serializers.ValidationError({ 'amount': 'Balance insuffisant' })
            return attrs
        except Wallet.DoesNotExist:
            raise serializers.ValidationError({ 'wallet': 'Invalid Wallet' }) from Wallet.DoesNotExist
