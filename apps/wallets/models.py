import uuid
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.agents.models import Agent
from apps.notifications.models import Notification

from apps.notifications.utils import send_push_message
from apps.wallets.utils import send_success_transfer_email

# Create your models here.
class Wallet(models.Model):
    """
    Wallet model
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.OneToOneField('events.Event', on_delete=models.CASCADE)
    usd_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cdf_balance = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Meta class
        """
        db_table = 'wallets'
        ordering = ['-created_at']
        verbose_name = 'Wallet'
        verbose_name_plural = 'Wallets'
        get_latest_by = 'updated_at'

    def __str__(self) -> str:
        return f'Wallet - {self.event.name}'

    def item(self) -> dict:
        """
        Returns a dict representation of the wallet
        """
        return {
            'id': str(self.id),
            'event': self.event.item(),
            'usd_balance': str(self.usd_balance),
            'cdf_balance': str(self.cdf_balance),
            'created_at': str(self.created_at)
        }

class TransferRequest(models.Model):
    """
    Transfer Request Model
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    phone_number = models.CharField(max_length=20, default='')
    executed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.wallet.event.name} - {self.amount}{self.currency}'

    def item(self) -> dict:
        """
        Returns a dict representation of the transfer request
        """
        return {
            'id': str(self.id),
            'wallet': self.wallet.item(),
            'amount': str(self.amount),
            'currency': self.currency,
            'phone_number': self.phone_number,
            'executed': self.executed,
            'created_at': str(self.created_at)
        }

@receiver(post_save, sender=TransferRequest)
def handle_transfer_request(sender, instance, created, **__): # pylint: disable=unused-argument
    """
    Handle transfer request.
    """
    if not created:
        if instance.executed:
            event_admin = Agent.objects.get(event__id=instance.wallet.event.id, role='admin')
            wallet = instance.wallet
            currency = instance.currency
            if str(currency).lower() == 'cdf':
                wallet.cdf_balance -= instance.amount
            else:
                wallet.usd_balance -= instance.amount
            wallet.save()
            notification = Notification(
                title="Votre demande de transfert a été traitée",
                body=f"Bonjour {event_admin.user.firstname}. \n \n Votre demande de transfert de {instance.amount}{instance.currency} a été traitée avec succès. \n \n Votre solde actuel est : \n {wallet.usd_balance} USD \n {wallet.cdf_balance} CDF.",
                data=instance.item()
            )
            notification.save()
            send_push_message(event_admin.user.notif_token, notification.title, notification.body, notification.data)
            send_success_transfer_email(event_admin.user.email)
