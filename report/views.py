from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
from .models import Report
from account.models import Account
from django.utils import timezone
from core.utils import LoginConfirm
import json

class CreateReport(View):
    @LoginConfirm
    def post(self,request):
        print("정현이 리퀘스트",request)
        data = json.loads(request.body)
        print("데이터",data)
        if Report.objects.filter(user=data['userId']).exists():
            detail = Report.objects.get(user=data['userId'])
            print("여기로?",detail)
            print(dir(detail))
            print("시간몇시냐?",timezone.now())
            detail.pub_date = timezone.now()
            detail.save()
        else :
            Report.objects.create(
                user = Account.objects.get(id=data['userId'])
            )
        return JsonResponse({"message: ":"ok"},status=200)
            
