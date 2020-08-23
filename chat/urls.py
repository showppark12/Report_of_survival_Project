from django.contrib import admin
from django.urls import path, include
from .views import Chat

urlpatterns = [
    path('<int:sender_id>', Chat.as_view()),
    path('<int:sender_id>', Chat.as_view()),
]
