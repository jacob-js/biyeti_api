from unicodedata import name
from django.db import models
import uuid

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name

class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='admin')
    name = models.CharField(max_length=255, null=False)
    cover = models.CharField(max_length=255)
    event_date = models.DateTimeField(null=False)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category', default=1)

    def __str__(self) -> str:
        return self.name

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
            'event': self.event,
            'name': self.name,
            'price': self.price,
            'currency': self.currency
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

    class Meta:
        unique_together = (('ticket', 'user', 'interval', 'available'))

    def __str__(self):
        return '{} {} {}'.format(self.ticket.place.name, self.ticket.price, self.ticket.currency)