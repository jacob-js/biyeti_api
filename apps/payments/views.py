import requests
import uuid
from rest_framework.decorators import api_view, permission_classes

from Utils.auth_utils import VerifyToken
from Utils.helpers import sendRes
from globals.config import PAYMENT_ENDPOINT, PAYMENT_MERCHANT, PAYMENT_TOKEN, SERVER_URL
from .serializers import PaymentRequestSerializer, PaymentSerializer

@api_view(['POST'])
@permission_classes([VerifyToken])
def initiate_payment(request):
    """
    Initiate payment
    """
    try:
        data = request.data
        serializer = PaymentSerializer(data={
            'user': request.user.id,
            **data
        })
        if serializer.is_valid():
            r = requests.post(PAYMENT_ENDPOINT, json={
                'phone': serializer.validated_data['phone'],
                'amount': str(serializer.validated_data['amount']),
                'currency': serializer.validated_data['currency'],
                'merchant': PAYMENT_MERCHANT,
                'type': 1,
                'reference': uuid.uuid4().hex,
                'callbackUrl': f'{SERVER_URL}/api/v1/payments/callback?event={serializer.validated_data["event"]}&user={request.user.id}&ticket={serializer.validated_data["ticket"]}',
            }, headers={
                'Authorization': f'Bearer {PAYMENT_TOKEN}',
                'content-type': 'application/json'
            })
            if(r.json()['code'] == "0"):
                return sendRes(201, msg='Payment initiated successfully')
            return sendRes(400, error=r.json()['message'])
        return sendRes(400, msg='Invalid request', error=serializer.errors)
    except:
        return sendRes(500, error='Internal server error') 

@api_view(['GET', 'POST'])
# @permission_classes([VerifyToken])
def callback(request):
    """
    Callback
    """
    print('Method : ', request.method)
    print('Data : ', request.data)
    print("Body : ", request.body)
    # try:
    #     data = request.data
    #     if data['status'] == 'success':
    #         requests.post(PAYMENT_ENDPOINT, data={
    #             'merchant': PAYMENT_MERCHANT,
    #             'type': 2,
    #             'reference': data['reference'],
    #             'status': data['status']
    #         })
    #         return sendRes(201, msg='Payment completed successfully')
    # except:
    #     return sendRes(500, error='Internal server error')   
    # return sendRes(500, error='Something went wrong')
