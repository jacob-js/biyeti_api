from rest_framework.decorators import api_view, permission_classes

from Utils.auth_utils import VerifyAdmin, VerifyToken
from Utils.helpers import sendRes
from apps.wallets.models import Wallet
from apps.wallets.serializers import WalletSerializer

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
