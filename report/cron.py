from .models import Report,DailyReportList
from chat.models import ChannelName,Chat_Message,ChatRoom
from django.utils import timezone

def my_cron_job():
    print("ㅎㅎ 크론탭 실행ㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎ")
    data= [{
            'id' : report_list.user.id,
            'name': report_list.user.name,
            'pub_date': report_list.pub_date.strftime('%Y-%m-%d %H:%M:%S'),
            'message' : report_list.message

        } for report_list in Report.objects.all().order_by('-pub_date')]
    
    DailyReportList.objects.create(
        date = timezone.now().strftime('%Y-%m-%d'),
        report_data = {
            "report_list":data
        }
    )

    Report.objects.all().delete()
    ChannelName.objects.all().delete()
    Chat_Message.objects.all().delete()
    ChatRoom.objects.all().delete()
