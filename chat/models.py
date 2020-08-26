from django.db import models

from account.models import Account

class ChannelName(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    channel_name = models.CharField(max_length=300)

    def __str__(self):
        return self.user.name

class ChatRoom(models.Model):
    req_user = models.ForeignKey(Account, related_name ="req_chatroom", on_delete=models.CASCADE)
    res_user = models.ForeignKey(Account, related_name ="res_chatroom", on_delete=models.CASCADE)

    req_channel_name = models.CharField(max_length=300)
    res_channel_name = models.CharField(max_length=300)

class Chat_Message(models.Model):
    room_id = models.ForeignKey(ChatRoom, related_name="chat_message", on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)
    sender = models.CharField(max_length=20)