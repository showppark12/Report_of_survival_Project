from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from .models import ChannelName, ChatRoom, Chat_Message
from account.models import Account


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
        print("ㅇㅇ?")

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

            room = ChatRoom.objects.create(
                req_user=Account.objects.get(id=self.sender_id),
                res_user=Account.objects.get(id=receiver_id),
                req_channel_name=self.channel_name,
                res_channel_name=receiver.channel_name
            )
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'room_id': room.id,
                    'sender_id' : self.sender_id,
                    'message': message
                }
            )
            Chat_Message.objects.create(
                room_id = room,
                text= message,
                sender= self.sender_id
            )
            self.send(text_data=json.dumps({
            'room_id': room.id
            }))
        elif text_data_json['type'] == 'MESSAGE':
            room_id = text_data_json['room_id']
            print("이거 뭐라고 들어오길래????", message)
            self.send(text_data=json.dumps({
                'message': message
            }))
            Chat_Message.objects.create(
                room_id = room_id,
                text= message,
                sender= self.sender_id
            )

    def chat_message(self, event):
        message = event['message']
        room_id = event['room_id']
        sender_id = event['sender_id']
        print("서버로 돌려줄 메세지 ",message)
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'room_id' :room_id,
            'sender_id' : sender_id,
            'message': message
        }))
