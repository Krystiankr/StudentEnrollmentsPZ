from django.contrib import admin
from django.urls import path

from app.views import LoginView, ChangePasswordView, ChangeGroupView, RequestsListView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),
    path("change-group/", ChangeGroupView.as_view(), name="change_group"),
    path("requests-list/", RequestsListView.as_view(), name="requests_list"),
]
