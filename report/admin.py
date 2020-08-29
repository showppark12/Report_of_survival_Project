from django.contrib import admin

from .models import Report, DailyReportList

admin.site.register(Report)
admin.site.register(DailyReportList)
