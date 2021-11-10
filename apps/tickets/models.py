from django.db import models
import uuid

# Create your models here.
class Place(models.Model):
    name = models.CharField(max_length=255, null=False)
    number = models.IntegerField(null=False)
    caption = models.CharField(max_length=255, null=True)

    def __str__(self) -> str:
        return f'{self.name} {self.number}'

    def item(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'number': self.number,
            'caption': self.caption
        }

class Ticket(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='place')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    currency = models.CharField(max_length=3, null=False)
    event_date = models.DateTimeField(null=False)

    def __str__(self):
        return '{} {}{}'.format(self.place.name, self.price, self.currency)
    
    class Meta:
        unique_together = (('place', 'event_date'))

class Purchase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='ticket')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='user')
    purchased_at = models.DateTimeField(auto_now_add=True)
    interval = models.IntegerField(default=0)

    class Meta:
        unique_together = (('ticket', 'user', 'interval'))

    def __str__(self):
        return '{} {} {}'.format(self.ticket.place.name, self.ticket.price, self.ticket.currency)