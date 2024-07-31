# import json
# from channels.generic.websocket import WebsocketConsumer


# class NotificationConsumer(WebsocketConsumer):
#     def connect(self): 
#         self.accept()
#         self.send(text_data=json.dumps({
#             'type': 'connection_established',
#             'message': 'You are succesfully connected'
#         }))
    
#     def send_notification(self, event):
#         print(event)
#         self.send(text_data=json.dumps({
#             'message': event['message']
#         }))
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'public_room'
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
        print(event)
        await self.send(text_data=json.dumps({ 'message': event['message'] }))