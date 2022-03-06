import datetime
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from Utils.auth_utils import VerifyAdmin, VerifyToken, checkIsAgent
from Utils.helpers import sendRes
from .serialzers import PurchasePostSerialzer, PurchaseSerializer, TicketPostSerialzer, TicketSerializer
from .models import Purchase, Ticket

# Create your views here.
class TicketsView(APIView):
    permission_classes = [VerifyToken, VerifyAdmin]
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()

    def get(self, request):
        serializer = self.serializer_class(self.queryset.all().order_by('event_date'), many=True)
        return sendRes(status=200, data=serializer.data)

    def post(self, request):
        serializer = TicketPostSerialzer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return sendRes(status=201, data=serializer.data, msg="Ticket enregistré")
        return sendRes(status=400, error=serializer.errors)

class TicketDetail(APIView):
    permission_classes = [VerifyToken]

    def get(self, request, id):
        try:
            ticket = Ticket.objects.get(id=id)
        except Ticket.DoesNotExist:
            return sendRes(status=404, error='Ticket not found')
        serializer = TicketSerializer(ticket)
        return sendRes(status=200, data=serializer.data)

    def put(self, request, id):
        try:
            ticket = Ticket.objects.get(id=id)
            ser = TicketSerializer(ticket)
        except Ticket.DoesNotExist:
            return sendRes(status=404, error='Ticket not found')
        serializer = TicketPostSerialzer(ticket)
        serializer.update(ticket, request.data)
        return sendRes(status=200, data=ser.data, msg="Modification enregistrée")

    def delete(self, request, id):
        try:
            ticket = Ticket.objects.get(id=id)
            ser = TicketSerializer(ticket)
            ticket.delete()
            return sendRes(status=204, msg="Billet supprimé")
        except Ticket.DoesNotExist:
            return sendRes(status=404, error='Ticket not found')


@api_view(['GET'])
@permission_classes([VerifyToken, VerifyAdmin])
def getPurchasesList(request):
    purchases = Purchase.objects.all().order_by('-purchased_at')
    serialzer = PurchaseSerializer(purchases, many=True)

    return sendRes(status=200, data=serialzer.data)

@api_view(['POST'])
@permission_classes([VerifyToken])
def createPurchase(request):
    try:
        ticket = Ticket.objects.get(id=request.data.get('ticket'))
        interval = (ticket.event_date + datetime.timedelta(hours=5)).timestamp()
        data = { **request.data, 'user': request.user.id, 'interval': interval }
    except:
        return sendRes(status=404, error="Billet incorrect")
    serialzer = PurchasePostSerialzer(data=data)
    serialzer.is_valid(raise_exception=True)
    ticket.place.number = ticket.place.number -1
    ticket.place.save()
    serialzer.save()
    return sendRes(status=201, msg="Achat effectué", data=serialzer.data)

@api_view(['GET'])
@permission_classes([VerifyToken])
def get_user_tickets(request, user_id):
    try:
        purchases = Purchase.objects.filter(user=user_id).order_by('-purchased_at')
        serialzer = PurchaseSerializer(purchases, many=True)
        return sendRes(200, data=serialzer.data)
    except:
        return sendRes(500, "Quelque chose s'est mal passée")

@api_view(['GET'])
@permission_classes([VerifyToken, checkIsAgent])
def check_ticket_status(request, id):
    try:
        ticket = Purchase.objects.get(id=id)
        serializer = PurchaseSerializer(ticket)
        date_now = datetime.datetime.now().timestamp()
        if ticket.interval < date_now:
            ticket.available=False
            ticket.save()
            return sendRes(403, "La validité du ticket a expiré", data=serializer.data)
        if ticket.availability != True:
            return sendRes(403, "Le ticket n'est plus valide", data=serializer.data)
        ticket.availability = False
        ticket.save()
        return sendRes(200, data=serializer.data)
    except:
        return sendRes(404, "Ticket introuvable")