import json
from django.views import View
from django.http import HttpResponse, JsonResponse

class Chat(View):
    def get(self, requset, sender_id):
        print("채팅보내는사람아이디",sender_id)
        return JsonResponse({"message":"해당유저의 채팅방리스트"}, status =200)

    def post(self, request, sender_id):
        data = json.loads(request.body)
        receiver_id = data['opposite_id']
        print("채팅만든사람 : ",sender_id)
        print("리시버아이디 : ",receiver_id)
        return JsonResponse({"message":"특정 채팅방들어옴"}, status=200)