from rest_framework.views import APIView
from Utils.auth_utils import VerifyAdmin, VerifyToken

from Utils.helpers import sendRes

from .serialzers import TicketPostSerialzer, TicketSerializer
from .models import Ticket

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