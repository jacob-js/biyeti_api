from channels.generic.websocket import AsyncJsonWebsocketConsumer

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
        print("user : ", user_id)
        self.channel_layer.group_add(user_id, self.channel_name)

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
