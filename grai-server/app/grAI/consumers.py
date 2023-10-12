# chat/consumers.py
import json

from channels.generic.websocket import AsyncConsumer, WebsocketConsumer
from asgiref.sync import async_to_sync


class ChatConsumer(WebsocketConsumer):
    """
    scope includes: path, headers, method, user, and url_route
    """

    def connect(self):
        user = self.scope["user"]
        self.user_id = user.id
        self.workspace = "workspace"  # gotta source this from auth somehow
        self.group_name = f"{self.user_id}-{self.workspace}"
        print(self.group_name)

        # if not user.is_authenticated:
        #    self.close()
        #    return

        # Using groups will allow us to broadcast to different browsers but we are limited to 100 simultaneous groups by default

        # Join group
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
        async_to_sync(self.channel_layer.group_send)(
            self.group_name, {"type": "chat.message", "message": f"Logged in as {self.group_name}"}
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(self.group_name, {"type": "chat.message", "message": message})

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))
