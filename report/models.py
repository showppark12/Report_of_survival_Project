from django.db import models
from account.models import Account

class Report(models.Model):
    user = models.ForeignKey(Account, related_name='survivor', on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    message = models.charField(max_length=100, blank=True)

    class Meta:
        db_table ='report'