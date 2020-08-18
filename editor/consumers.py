import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        #message = text_data_json['message']
        op = text_data_json['operation']
        pos = text_data_json['position']
        letter = text_data_json['letter']
        name = text_data_json['name']
        time = text_data_json['time']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'operation': op,
                'position': pos,
                'letter': letter,
                'name': name,
                'time': time
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        #message = event['message']
        op = event['operation']
        pos = event['position']
        letter = event['letter']
        name = event['name']
        time = event['time']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'operation': op,
            'position': pos,
            'letter': letter,
            'name': name,
            'time': time
        }))