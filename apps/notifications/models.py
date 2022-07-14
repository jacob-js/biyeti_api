from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from firebase_admin import messaging

from apps.tickets.models import Purchase

# Create your models here.
class Notification(models.Model):
    """
    Model for storing notification information.
    """
    title = models.CharField(max_length=255)
    body = models.TextField()
    data = models.JSONField(default=None, null=True, blank=True)
    notification_type = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, default='unread')
    user_receiver = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='notifications')

    def item(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'data': self.data,
            'notification_type': self.notification_type,
            'status': self.status,
            'user_receiver': self.user_receiver.item()
        }


@receiver(post_save, sender=Purchase)
def handle_new_purchase(sender, instance, created, **__): # pylint: disable=unused-argument
    """
    Handle new purchase.
    """
    if created:
        notification = Notification(
            title='Nouvel achat du billet',
            body=f'Vous avez acheté un billet pour l\'événement {instance.ticket.event.name}',
            data={
                'purchase': instance.item()
            },
            notification_type='new_purchase',
            user_receiver=instance.user
        )
        notification.save()
        message = messaging.Message(notification=messaging.Notification(
            title='Nouvel achat du billet',
            body=notification.body,
        ), token=instance.user.fcm_token)
        messaging.send(message=message)
        