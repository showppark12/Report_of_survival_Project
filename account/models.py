from django.db import models
from django.utils import timezone

class Account(models.Model):
    email = models.EmailField(max_length=128)
    name = models.CharField(max_length = 50)
    password = models.CharField(max_length = 200)
    created_at = models.DateTimeField(default=timezone.now)
    description = models.CharField(max_length =300, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'accoutns'