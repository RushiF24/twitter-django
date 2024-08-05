import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer

from .serializers import NotificationListSerializer
class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        id = self.scope.get('url_route', {}).get(
                'kwargs').get('id')
        self.group_name = f'notification_from_{id}_to_user'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def send_notification(self, event):
        print("-----------------------------------")
        await self.send(text_data=json.dumps({ 'data': event['notification']}))