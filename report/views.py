from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
from .models import Report,DailyReportList
from account.models import Account
from django.utils import timezone
from core.utils import LoginConfirm
import json

class CreateReport(View):
    @LoginConfirm
    def post(self,request):
        now = timezone.now().strftime('%H')
        # int(now) >= 6 and int(now)<24
        if False:
            return JsonResponse({"message":"서버이용시간이아닙니다."},status=400)
        else:
            data = json.loads(request.body)
            if Report.objects.filter(user=data['userId']).exists():
                detail = Report.objects.get(user=data['userId'])
                detail.pub_date = timezone.now()
                detail.save()
            else :
                Report.objects.create(
                    user = Account.objects.get(id=data['userId'])
                )
            return JsonResponse({"message":"ok"},status=200)
            
class ReportList(View):
    @LoginConfirm
    def get(self,request):
        data= [{
            'id' : report_list.user.id,
            'name': report_list.user.name,
            'pub_date': report_list.pub_date.strftime('%Y-%m-%d %H:%M:%S'),
            'message' : report_list.message

        } for report_list in Report.objects.all().order_by('-pub_date')]
        return JsonResponse({"report_list":data}, status=200)

def DailyReport(self,request):
    data = DailyReportList.objects.get(date=timezone.now().strftime('%Y-%m-%d'))
    return JsonResponse({"report_list":data}, status = 200)