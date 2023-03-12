from django.contrib import admin
from django.urls import path

from app.views import IndexView, StudentsView, GroupsView

urlpatterns = [
    path("", IndexView.as_view(), name='login'),
    path("students", StudentsView.as_view(), name='students'),
    path("groups", GroupsView.as_view(), name='groups'),
]
