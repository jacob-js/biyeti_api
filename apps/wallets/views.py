from rest_framework.decorators import api_view, permission_classes

from Utils.auth_utils import CheckIsAgent, CheckIsEventAdmin, VerifyAdmin, VerifyToken
from Utils.decorators.confirm_pwd import check_pwd
from Utils.helpers import sendRes
from apps.agents.models import Agent
from apps.wallets.models import TransferRequest, Wallet
from apps.wallets.serializers import TransferRequestSerializer, WalletSerializer
from apps.wallets.utils import send_request_transfer_email, send_success_transfer_email

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
@check_pwd
def request_wallet_balance_transfer(request, event_id):
    """
    Request wallet balance transfer
    """
    try:
        wallet = Wallet.objects.get(event__id=event_id)
        serializer = TransferRequestSerializer(data={**request.data, 'wallet': wallet.id})
        if not serializer.is_valid():
            return sendRes(400, msg='Invalid request', error=serializer.errors)
        serializer.save()
        send_request_transfer_email()
        return sendRes(200, msg='Balance transfer requested')
    except Wallet.DoesNotExist:
        return sendRes(404, error='Wallet not found')
    except:
        return sendRes(500, error='Internal server error')


@api_view(['POST'])
@permission_classes([VerifyToken, VerifyAdmin])
def execute_balance_transfer_request(_, request_id):
    """
    Execute transfer request
    """
    try:
        transfer_request = TransferRequest.objects.get(id=request_id)
        transfer_request.executed = True
        transfer_request.save()
        wallet = Wallet.objects.get(id=transfer_request.wallet.id)
        currency = transfer_request.currency
        wallet[f'{str(currency).lower()}_balance']-= transfer_request.amount
        wallet.save()
        event_admin = Agent.objects.get(event__id=wallet.event.id, role='admin')
        send_success_transfer_email(event_admin.user.email)
        return sendRes(200, msg="Operation done")
    except TransferRequest.DoesNotExist:
        return sendRes(404, "Request not found")
    except:
        return sendRes(500, "Something went wrong")