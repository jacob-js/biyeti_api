from rest_framework.decorators import api_view, permission_classes

from Utils.auth_utils import CheckIsAgent, CheckIsEventAdmin, VerifyAdmin, VerifyToken
from Utils.helpers import sendRes
from apps.wallets.models import Wallet
from apps.wallets.serializers import TransferRequestSerializer, WalletSerializer
from apps.wallets.utils import send_request_transfer_email

# Create your views here.
@api_view(['GET'])
@permission_classes([VerifyToken, VerifyAdmin])
def get_wallets(_):
    """
    Get wallets
    """
    try:
        wallets = Wallet.objects.all()
        serializer = WalletSerializer(wallets, many=True)
        return sendRes(200, data=serializer.data)
    except:
        return sendRes(500, error='Internal server error')

@api_view(['GET'])
@permission_classes([VerifyToken, CheckIsAgent, CheckIsEventAdmin])
def get_event_wallet(_, event_id):
    """
    Get event wallet
    """
    try:
        wallet = Wallet.objects.get(event__id=event_id)
        serializer = WalletSerializer(wallet)
        return sendRes(200, data=serializer.data)
    except Wallet.DoesNotExist:
        return sendRes(404, error='Wallet not found')
    except:
        return sendRes(500, error='Internal server error')


@api_view(['POST'])
@permission_classes([VerifyToken, CheckIsAgent, CheckIsEventAdmin])
def request_wallet_balance_transfer(request, event_id):
    """
    Request wallet balance transfer
    """
    try:
        wallet = Wallet.objects.get(event__id=event_id)
        serializer = TransferRequestSerializer(data={**request.data, 'wallet': wallet.id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        send_request_transfer_email()
        return sendRes(200, data={'message': 'Balance transfer requested'})
    except Wallet.DoesNotExist:
        return sendRes(404, error='Wallet not found')
    except:
        return sendRes(500, error='Internal server error')
