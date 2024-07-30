import json
from channels.generic.websocket import WebsocketConsumer


class NotificationConsumer(WebsocketConsumer):
    def connect(self): 
        self.accept()
        self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'You are succesfully connected'
        }))
    
    def send_notification(self, event):
        print(event)
        self.send(text_data=json.dumps({
            'message': event['message']
        }))