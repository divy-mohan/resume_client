import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Order, ChatMessage

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.order_id = self.scope['url_route']['kwargs']['order_id']
        self.room_group_name = f'chat_{self.order_id}'
        
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
        message_type = text_data_json.get('type', 'message')
        
        if message_type == 'message':
            message = text_data_json['message']
            user_id = text_data_json['user_id']
            is_admin = text_data_json.get('is_admin', False)
            
            # Save message to database
            await self.save_message(user_id, message, is_admin)
            
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'user_id': user_id,
                    'is_admin': is_admin,
                }
            )
        elif message_type == 'typing':
            user_id = text_data_json['user_id']
            is_typing = text_data_json['is_typing']
            
            # Send typing indicator to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'typing_indicator',
                    'user_id': user_id,
                    'is_typing': is_typing,
                }
            )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        user_id = event['user_id']
        is_admin = event['is_admin']
        
        # Get user name
        user_name = await self.get_user_name(user_id, is_admin)
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'user_name': user_name,
            'is_admin': is_admin,
        }))

    @database_sync_to_async
    def save_message(self, user_id, message, is_admin):
        user = User.objects.get(id=user_id)
        order = Order.objects.get(id=self.order_id)
        ChatMessage.objects.create(
            user=user,
            order=order,
            message=message,
            is_admin=is_admin
        )

    # Handle typing indicator
    async def typing_indicator(self, event):
        user_id = event['user_id']
        is_typing = event['is_typing']
        
        # Get user name
        user_name = await self.get_user_name(user_id, False)
        
        # Send typing indicator to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'user_name': user_name,
            'is_typing': is_typing,
        }))

    @database_sync_to_async
    def get_user_name(self, user_id, is_admin):
        if is_admin:
            return "Support Team"
        user = User.objects.get(id=user_id)
        return user.get_full_name()