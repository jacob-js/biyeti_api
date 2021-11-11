import datetime
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from Utils.auth_utils import VerifyAdmin, VerifyToken
from Utils.helpers import sendRes
from .serialzers import PlaceSerialzer, PurchasePostSerialzer, PurchaseSerializer, TicketPostSerialzer, TicketSerializer
from .models import Place, Purchase, Ticket

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
            return sendRes(status=201, data=serializer.data)
        return sendRes(status=400, data=serializer.errors)

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

class PlacesView(APIView):
    permission_classes = [VerifyToken]

    def get(self, request):
        places = Place.objects.all()
        serialzer = PlaceSerialzer(places, many=True)
        return sendRes(200, None, data=serialzer.data)

    def post(self, request):
        serialzer = PlaceSerialzer(data=request.data)
        serialzer.is_valid(raise_exception=True)
        serialzer.save()
        return sendRes(201, msg='Place ajoutée', data=serialzer.data)

class PlaceDetailView(APIView):
    permission_classes = [VerifyToken]

    def get(self, request, id):
        try:
            place = Place.objects.get(id=id)
            serialzer = PlaceSerialzer(place)
            return sendRes(status=200, data=serialzer.data)
        except:
            return sendRes(404, "Place non trouvée")

    def put(self, request, id):
        try:
            place = Place.objects.get(id=id)
            serialzer = PlaceSerialzer(place)
            serialzer.update(place, request.data)
            return sendRes(status=200, data=serialzer.data)
        except:
            return sendRes(404, "Place non trouvée")

    def delete(self, request, id):
        try:
            place = Place.objects.get(id=id)
            place.delete()
            return sendRes(status=204, msg="Place supprimée")
        except:
            return sendRes(404, "Place non trouvée")


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
        interval = (ticket.event_date + datetime.timedelta(hours=6)).timestamp()
        data = { **request.data, 'user': request.user.id, 'interval': interval }
    except:
        return sendRes(status=404, error="Billet incorrect")
    serialzer = PurchasePostSerialzer(data=data)
    serialzer.is_valid(raise_exception=True)
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