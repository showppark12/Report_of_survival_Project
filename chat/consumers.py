from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.command = self.scope['url_route']['kwargs']['command']
        print("커맨드들어오냐?",self.command)
        if self.command=="connect":
            print("여기론안오지?")
            self.sender_id = self.scope['url_route']['kwargs']['sender_id']
            print(self.sender_id)
            self.accept()
        elif self.command[:6]=="create":
            receiver_id = self.command[:6]
            print("본인 채널",self.channel_name)
            print("채팅방에 초대시킬 상대 ",receiver_id)
            self.room_group_name = "asdf"
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print("이거 뭐라고 들어오길래????",message)

        self.send(text_data=json.dumps({
            'message': message
        }))