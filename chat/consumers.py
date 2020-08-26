from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from .models import ChannelName, ChatRoom, Chat_Message
from account.models import Account
from django.core.serializers.json import DjangoJSONEncoder

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.sender_id = self.scope['url_route']['kwargs']['sender_id']
        print("로그인한사람 아이디", self.sender_id)
        print("본인 채널", self.channel_name)
        ChannelName.objects.create(
            user=Account.objects.get(id=self.sender_id),
            channel_name=self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        print("여기까진와?", text_data)
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        self.sender_id = self.scope['url_route']['kwargs']['sender_id']
        receiver_id = text_data_json['receiver_id']
        if text_data_json['type'] == 'INITIAL':
            self.room_group_name = "chat_%s_%s" % (self.sender_id, receiver_id)
            print("라사보",receiver_id)
            receiver = ChannelName.objects.get(user=receiver_id)
            print("리시버 가져오냐?", receiver)
            print("리시버 채널네임 가져오냐?", receiver.channel_name)

            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                receiver.channel_name
            )
            print("여기까진?")
            room = ChatRoom.objects.create(
                req_user=Account.objects.get(id=self.sender_id),
                res_user=Account.objects.get(id=receiver_id)
            )
            print("여기까진?2")
            send_message = Chat_Message.objects.create(
                room_id=room,
                text=message,
                sender=room.req_user.id
            )
            print("여기까진?3")
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type' : 'chat_message',
                    '_id': send_message.id,
                    'sender_id': send_message.room_id.req_user.id,
                    'message': message,
                    'room_id' : send_message.room_id.id
                }
            )
        elif text_data_json['type'] == 'MESSAGE':
            room_id = text_data_json['room_id']
            self.sender_id = self.scope['url_route']['kwargs']['sender_id']
            print("이거 뭐라고 들어오길래????", message)
            sender = Account.objects.get(id=self.sender_id)
            send_message = Chat_Message.objects.create(
                room_id=room_id,
                text=message,
                sender=sender.name,
            )
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    '_id' : send_message.id,
                    'room_id': room_id,
                    'sender_id': sender.id,
                    'message': message,
                    'create_at': send_message.created_at
                }
            )

    def chat_message(self, event):
        print("이벤트",event)
        message = event['message']
        _id = event['_id']
        sender_id = event['sender_id']
        room_id = event['room_id']
        chat_message = Chat_Message.objects.get(id = _id)
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            '_id': _id,
            'text' : message,
            'createdAt' : chat_message.created_at,
            'user': {
                '_id': sender_id
            },
            'room_id' : room_id
        },cls=DjangoJSONEncoder))
