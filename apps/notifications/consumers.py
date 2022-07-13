from channels.generic.websocket import AsyncJsonWebsocketConsumer

from apps.notifications.models import Notification
from apps.notifications.serializers import NotificationSerializer

class UserNotificationConsumer(AsyncJsonWebsocketConsumer):
    """
    This consumer is used to send a request to the Ntification API.
    """

    async def connect(self):
        """
        Connect to the Notification server.
        """
        await self.accept()
        print("Connected to Nt")
        user_id = self.scope['url_route']['kwargs']['user_id']
        notifications = Notification.objects.filter(user_receiver__id=user_id)
        serializer = NotificationSerializer(notifications, many=True)
        self.channel_layer.groud_ad(user_id, self.channel_name)
        self.send_json(serializer.data)

    async def disconnect(self, _):
        """
        Disconnect from the Notification server.
        """
        user_id = self.scope['url_route']['kwargs']['user_id']
        self.channel_layer.group_discard(user_id, self.channel_name)

    async def new_notif(self, event):
        """
        Send a new notification to the client.
        """
        print("socket : ", event)
        await self.send_json(event)
