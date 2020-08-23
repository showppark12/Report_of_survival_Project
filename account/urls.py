from django.urls import path, include
from .views import SignUpView, SignIn, AccountView, Activate, Email

urlpatterns = [
    path('validation', AccountView.as_view()),
    path('sign-up', SignUpView.as_view()),
    path('sign-in', SignIn.as_view()),
    path('activate/<str:uidb64>/<str:token>', Activate.as_view()),
    path('email', Email.as_view()),
]
