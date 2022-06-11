import uuid
from django.db import models
from apps.events.models import Event

# Create your models here.
class Ticket(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event', null=True)
    name = models.CharField(max_length=255, null=True)
    number_of_place = models.IntegerField(null=True)
    caption = models.CharField(max_length=255, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    currency = models.CharField(max_length=3, null=True)

    def __str__(self):
        return '{} {}{}'.format(self.name, self.price, self.currency)

    def item(self) -> dict:
        return {
            'id': self.id,
            'event': self.event.item(),
            'name': self.name,
            'price': self.price,
            'currency': self.currency,
            'number_of_place': self.number_of_place,
            'caption': self.caption
        }
    
    class Meta:
        unique_together = (('event', 'name'))

class Purchase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='ticket')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='user')
    purchased_at = models.DateTimeField(auto_now_add=True)
    interval = models.FloatField(default=0)
    available = models.BooleanField(default=True)

    # class Meta:
    #     unique_together = (('ticket', 'user', 'interval', 'available'))

    def __str__(self):
        return '{} {} {}'.format(self.ticket.name, self.ticket.price, self.ticket.currency)