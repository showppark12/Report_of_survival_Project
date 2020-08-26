from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/chat/<int:sender_id>', consumers.ChatConsumer),
]