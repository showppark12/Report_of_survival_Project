from django.urls import path, include
from .views import CreateReport

urlpatterns = [
    path('',CreateReport.as_view()),
]
