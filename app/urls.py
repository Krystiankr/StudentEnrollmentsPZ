from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path

from app import views
from app.forms import LoginForm
from app.views import (
    IndexView,
    StudentsView,
    GroupsView,
    send_message,
    RegisterView,
    ProfileView,
    ProfileLogout,
    LoginView,
    ChatMain,
    ChatPrivate,
)

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("/", IndexView.as_view(), name="default"),
    path("students", StudentsView.as_view(), name="students"),
    path("send_message", send_message, name="send_message"),
    path("groups", GroupsView.as_view(), name="groups"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", ProfileLogout.as_view(), name="logout"),
    path("register", RegisterView.as_view(), name="register"),
    path("chat_main", ChatMain.as_view(), name="chat_main"),
    path("chat_private", ChatPrivate.as_view(), name="chat_private"),
    path("group_report/", views.group_report, name="group_report"),
]
