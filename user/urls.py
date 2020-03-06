# from django.contrib.auth.views import LoginView
from django.urls import path
from .views import LoginView, LogoutView, UserInfoView, ChangePasswordView

urlpatterns = [
    path("login/", LoginView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("info/", UserInfoView.as_view()),
    path("password/", ChangePasswordView.as_view()),
]