from django.db import models
from django.utils import timezone

from account.models import Account

class Report(models.Model):
    user = models.ForeignKey(Account, related_name='survivor', on_delete=models.CASCADE)
    pub_date = models.DateTimeField(default=timezone.now)
    message = models.CharField(max_length=100, blank=True)

    def __str__(self):
            return self.user.name

    class Meta:
        db_table ='report'

class DailyReportList(models.Model):
    date = models.DateTimeField()
    report_data = models.JSONField()

    def __str__(self):
        return self.date