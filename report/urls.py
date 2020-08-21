from django.urls import path, include
from .views import CreateReport,ReportList

urlpatterns = [
    path('',CreateReport.as_view()),
    path('list',ReportList.as_view()),
]
