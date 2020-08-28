from django.db import models
from django.utils import timezone
from account.models import Account
from channels.db import database_sync_to_async

class ChannelName(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    channel_name = models.CharField(max_length=300)

class ChatRoom(models.Model):
    room_name = models.CharField(max_length=200)
    req_user = models.ForeignKey(Account, related_name ="req_chatroom", on_delete=models.CASCADE)
    res_user = models.ForeignKey(Account, related_name ="res_chatroom", on_delete=models.CASCADE)
    
    def last_message(self):
        last_message =  Chat_Message.objects.filter(room_id = self.id)
        last_message.last()
        return last_message.last()

class Chat_Message(models.Model):
    room_id = models.ForeignKey(ChatRoom, related_name="chat_message", on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)
    sender = models.CharField(max_length=20)
    created_at = models.DateTimeField(default=timezone.now)