from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import ChannelName, ChatRoom, Chat_Message
from account.models import Account
from report.models import Report
from django.core.serializers.json import DjangoJSONEncoder
from channels.db import database_sync_to_async
import asyncio
from asgiref.sync import sync_to_async
from django.utils import timezone

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
                'message_type':"SYSTEM",
                'relogin': True
            }))
            await self.channel_layer.group_add(
                    "report",
                    self.channel_name
                )
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
        self.sender_id = self.scope['url_route']['kwargs']['sender_id']
        if text_data_json['type'] == 'REPORT':
            # now = timezone.now().strftime('%H')
            # int(now) >= 6 and int(now)<15
            print("현재 시각은?",now)
            if False:
                await self.send(text_data=json.dumps({
                    "message_type" : "SYSTEM",
                    'message': "서비스 이용시간이 아닙니다."
                }))
            else:
                if await database_sync_to_async(Report.objects.filter(user=self.sender_id).exists)():
                    detail = await database_sync_to_async(Report.objects.get)(user=self.sender_id)
                    detail.pub_date = timezone.now()
                    await database_sync_to_async(detail.save)()
                else:
                    await database_sync_to_async(Report.objects.create)(
                        user= await database_sync_to_async(Account.objects.get)(id=self.sender_id)
                    )
                    await self.channel_layer.group_add(
                        "report",
                        self.channel_name
                    )
                await self.channel_layer.group_send(
                    "report",
                    { 
                        "type" : "chat.message",
                        "real_type": "report",
                        "reporter" : self.sender_id
                    } 
                    )
                print("더이")
        elif text_data_json['type'] == 'INITIAL':
            message = text_data_json['message']
            receiver_id = text_data_json['receiver_id']
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
                room_name=self.room_group_name,
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
                    'real_type': "message",
                    '_id': send_message.id,
                    'sender_id': send_message.room_id.req_user.id,
                    'message': message,
                    'room_id': send_message.room_id.id
                }
            )
        elif text_data_json['type'] == 'MESSAGE':
            relogin = text_data_json['relogin']
            message = text_data_json['message']
            print("리로그인", relogin)
            room_id = text_data_json['room_id']
            cr = await database_sync_to_async(ChatRoom.objects.get)(id=room_id)
            self.sender_id = self.scope['url_route']['kwargs']['sender_id']
            if relogin == True:
                await self.channel_layer.group_add(
                    cr.room_name,
                    self.channel_name
                )
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
                cr.room_name,
                {
                    'type': 'chat.message',
                    'real_type': "message",
                    '_id': send_message.id,
                    'room_id': room_id,
                    'sender_id': sender.id,
                    'message': message,
                }
            )
            print("여기는?103")

    async def chat_message(self, event):
        print("이벤트", event)
        msg_type = event['real_type']
        print(msg_type)
        if msg_type == "report":
            reporter = event['reporter']
            await self.send(text_data=json.dumps({
            "message_type" : "REPORT",
            "reporter" : reporter
        }))
        else:
            _id = event['_id']
            sender_id = event['sender_id']
            room_id = event['room_id']
            message= event['message']
            chat_message = await database_sync_to_async(Chat_Message.objects.get)(id=_id)
            pub_datetime =chat_message.created_at.strftime('%Y-%m-%d %H:%M')
            print("ㅍ펍데이트타임",pub_datetime)
            # Send message to WebSocket
            await self.send(text_data=json.dumps({
                "message_type" : "MESSAGE",
                '_id': _id,
                'text': message,
                'relogin':False,
                'createdAt': pub_datetime,
                'user': {
                    '_id': sender_id
                },
                'room_id': room_id
            }))

    async def report_list(self, event):
        print("이벤트", event)
        report_list = event['message_type']
        print(report_list)
        # Send message to WebSocket
        # await self.send(text_data=json.dumps({
            
        # }))