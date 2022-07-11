import uuid
from django.db import models

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
            'usd_balance': self.usd_balance,
            'cdf_balance': self.cdf_balance,
            'created_at': self.created_at
        }
