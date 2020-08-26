from django.contrib import admin

from .models import ChannelName, ChatRoom, Chat_Message

admin.site.register(ChannelName)
admin.site.register(ChatRoom)
admin.site.register(Chat_Message)