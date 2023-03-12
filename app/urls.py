from django.contrib import admin
from django.urls import path

from app.views import IndexView, StudentsView, GroupsView, send_message

urlpatterns = [
    path("", IndexView.as_view(), name='login'),
    path("students", StudentsView.as_view(), name='students'),
    path('send_message', send_message, name='send_message'),
    path("groups", GroupsView.as_view(), name='groups'),
]
