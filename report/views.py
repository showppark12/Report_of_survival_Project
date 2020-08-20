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
        data = json.loads(request.body)
        print(data)
        surv = Account.objects.get(email=data['email'])
        print("얘는 값이머임?",surv)
        Report.objects.create(
            user= surv
        )
        return JsonResponse({"message: ":"ok"},status=200)
            
