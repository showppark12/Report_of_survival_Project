import json
from django.views import View
from django.http import HttpResponse, JsonResponse
from .models import ChatRoom, Chat_Message
from account.models import Account

class Chat(View):
    def get(self, request, sender_id):
        req_chat_list = ChatRoom.objects.filter(req_user=sender_id)
        req_data= [{
            "receiver_id" : chat.res_user.id,
            "receiver_name" : chat.res_user.name,
            "last_message" :  chat.last_message().text,
            "last_message_time" : chat.last_message().created_at.strftime('%Y-%m-%d %H:%M')
        } for chat in req_chat_list]
        res_chat_list = ChatRoom.objects.filter(res_user=sender_id)
        res_data= [{
            "receiver_id" : chat.req_user.id,
            "receiver_name" : chat.req_user.name,
            "last_message" :  chat.last_message().text,
            "last_message_time" : chat.last_message().created_at.strftime('%Y-%m-%d %H:%M')
        } for chat in res_chat_list]
        data= req_data + res_data
        data.sort(key=lambda ChatRoom: ChatRoom['last_message_time'],reverse= True)
        return JsonResponse({"chatroom_list": data}, status =200)

    def post(self, request, sender_id):
        data = json.loads(request.body)
        print("받는 데이터",data)
        receiver_id = data['receiver_id']
        print("채팅만든사람 : ",sender_id)
        print("리시버아이디 : ",receiver_id)
        if ChatRoom.objects.filter(req_user=sender_id,res_user=receiver_id).exists():
            chat_detail = ChatRoom.objects.get(req_user=sender_id,res_user=receiver_id)
        elif ChatRoom.objects.filter(res_user=sender_id,req_user=receiver_id).exists():
            chat_detail = ChatRoom.objects.get(res_user=sender_id,req_user=receiver_id)
        else:
            receiver = Account.objects.get(id =receiver_id)
            return JsonResponse({
                "messages":[]
        }, status=200)

        print("어디까지돼?")
        data= [{
            "_id" : detail.id,
            "text" : detail.text,
            "createdAt" : detail.created_at.strftime('%Y-%m-%d %H:%M'),
            "user" : {
                "_id" : int(detail.sender)
            },
            "room_id" : detail.room_id.id
        } for detail in Chat_Message.objects.filter(room_id = chat_detail).order_by('-created_at')]
        print("??")
        print(data)
        return JsonResponse({"messages":data}, status=200)