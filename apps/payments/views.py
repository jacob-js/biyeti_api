import requests
import uuid
from rest_framework.decorators import api_view, permission_classes

from Utils.auth_utils import VerifyToken, create_token
from Utils.helpers import sendRes
from apps.payments.models import Payment
from globals.config import PAYMENT_ENDPOINT, PAYMENT_MERCHANT, PAYMENT_TOKEN, SERVER_URL
from .serializers import PaymentSerializer

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
            serializer.save()
            payment_request = requests.post(PAYMENT_ENDPOINT, json={
                'phone': serializer.validated_data['phone'],
                'amount': str(serializer.validated_data['amount']),
                'currency': serializer.validated_data['currency'],
                'merchant': PAYMENT_MERCHANT,
                'type': 1,
                'reference': serializer.data.get('id'),
                'callbackUrl': f'{SERVER_URL}/api/v1/payments/callback',
            }, headers={
                'Authorization': f'Bearer {PAYMENT_TOKEN}',
                'content-type': 'application/json'
            })
            if payment_request.json()['code'] == "0":
                return sendRes(201, msg='Payment initiated successfully')
            return sendRes(400, error=payment_request.json()['message'])
        return sendRes(400, msg='Invalid request', error=serializer.errors)
    except:
        return sendRes(500, error='Internal server error')

@api_view(['POST'])
def callback(request):
    """
    Callback
    """
    try:
        data = request.data
        if data['code'] == "0":
            payment = Payment.objects.get(id=data['reference'])
            payment.paid = True
            payment.save()
            user = payment.user
            ticket = payment.ticket
            token = create_token(user.id)
            requests.post(f'{SERVER_URL}/api/v1/tickets/buy', json={
                'ticket': ticket,
                'payment': payment.id
            }, headers={
                'authtoken': token,
                'content-type': 'application/json'
            })
            return sendRes(201, msg='Ticket successfully bought')
        return sendRes(400, error="Can't perform payment")
    except:
        return sendRes(500, error='Internal server error')
