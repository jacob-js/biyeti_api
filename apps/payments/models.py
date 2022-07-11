import uuid
from django.db import models

# Create your models here.
class Payment(models.Model):
    """
    Payment model
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    canal = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=255)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    event = models.ForeignKey('events.Event', on_delete=models.CASCADE)
    ticket = models.ForeignKey('tickets.Ticket', on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'payments'
        ordering = ['-created_at']
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        get_latest_by = 'created_at'

    def __str__(self) -> str:
        return f'{self.user.username} - {self.event.name} - {self.ticket.name}'

    def item(self) -> dict:
        """
        Returns a dict representation of the payment
        """
        return {
            'id': str(self.id),
            'amount': self.amount,
            'currency': self.currency,
            'user': self.user.item(),
            'event': self.event.item(),
            'ticket': self.ticket.item(),
            'created_at': self.created_at
        }
