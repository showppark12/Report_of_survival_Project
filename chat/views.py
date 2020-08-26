import json
from django.views import View
from django.http import HttpResponse, JsonResponse
from .models import ChatRoom

class Chat(View):
    def get(self, requset, sender_id):
        chat_list = ChatRoom.objects.filter(req_user=sender_id) | ChatRoom.objects.filter(req_user=sender_id)
        return JsonResponse({"message": list(chat_list)}, status =200)

    def post(self, request, sender_id):
        data = json.loads(request.body)
        receiver_id = data['opposite_id']
        print("채팅만든사람 : ",sender_id)
        print("리시버아이디 : ",receiver_id)
        return JsonResponse({"message":"특정 채팅방들어옴"}, status=200)