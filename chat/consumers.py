from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import ChannelName, ChatRoom, Chat_Message
from account.models import Account
from django.core.serializers.json import DjangoJSONEncoder
from channels.db import database_sync_to_async
import asyncio


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.sender_id = self.scope['url_route']['kwargs']['sender_id']
        print("sender아이디", self.sender_id)
        if await database_sync_to_async(ChannelName.objects.filter(user=self.sender_id).exists)():
            channel = await database_sync_to_async(ChannelName.objects.get)(user=self.sender_id)
            channel.channel_name = self.channel_name
            await database_sync_to_async(channel.save)()
            await self.accept()
            await self.send(text_data=json.dumps({
                'relogin': True
            }))
        else:
            await database_sync_to_async(ChannelName.objects.create)(
                user=await database_sync_to_async(Account.objects.get)(id=self.sender_id),
                channel_name=self.channel_name
            )
            await self.accept()
        

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        print("여기까진와?", text_data)
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        self.sender_id = self.scope['url_route']['kwargs']['sender_id']
        receiver_id = text_data_json['receiver_id']
        if text_data_json['type'] == 'INITIAL':
            self.room_group_name = "chat_%s_%s" % (self.sender_id, receiver_id)
            print("룸그룹이름", self.room_group_name)
            print("라사보", receiver_id)
            receiver = await database_sync_to_async(ChannelName.objects.get)(user=receiver_id)

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.channel_layer.group_add(
                self.room_group_name,
                receiver.channel_name
            )
            print("여기까진?")
            room = await database_sync_to_async(ChatRoom.objects.create)(
                req_user=await database_sync_to_async(Account.objects.get)(id=self.sender_id),
                res_user=await database_sync_to_async(Account.objects.get)(id=receiver_id)
            )
            print("여기까진?2")
            send_message = await database_sync_to_async(Chat_Message.objects.create)(
                room_id=room,
                text=message,
                sender=room.req_user.id
            )
            print("여기까진?3")
            print("셀프레이어", self.channel_layer)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat.message',
                    '_id': send_message.id,
                    'sender_id': send_message.room_id.req_user.id,
                    'message': message,
                    'room_id': send_message.room_id.id
                }
            )
        elif text_data_json['type'] == 'MESSAGE':
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            room_id = text_data_json['room_id']
            self.room_group_name = "chat_%s_%s" % (self.sender_id, receiver_id)
            print("여기선?룸그룹이름", self.room_group_name)
            print(room_id)
            self.sender_id = self.scope['url_route']['kwargs']['sender_id']
            print("이거 뭐라고 들어오길래????", message)
            sender = await database_sync_to_async(Account.objects.get)(id=self.sender_id)
            print("여기까진오니?101")
            send_message = await database_sync_to_async(Chat_Message.objects.create)(
                room_id=await database_sync_to_async(ChatRoom.objects.get)(id=room_id),
                text=message,
                sender=sender.id,
            )
            print("여기는?102")
            print("셀프레이어", self.channel_layer)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat.message',
                    '_id': send_message.id,
                    'room_id': room_id,
                    'sender_id': sender.id,
                    'message': message,
                }
            )
            print("여기는?103")

    async def chat_message(self, event):
        print("이벤트", event)
        message = event['message']
        _id = event['_id']
        sender_id = event['sender_id']
        room_id = event['room_id']
        chat_message = await database_sync_to_async(Chat_Message.objects.get)(id=_id)
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            '_id': _id,
            'text': message,
            'createdAt': chat_message.created_at.strftime('%H:%M'),
            'user': {
                '_id': sender_id
            },
            'room_id': room_id
        }))
