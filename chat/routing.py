from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/chat/<int:sender_id>/<str:command>', consumers.ChatConsumer),
    path('ws/chat/<int:sender_id>/<int:receiver_id>', consumers.ChatConsumer)
]