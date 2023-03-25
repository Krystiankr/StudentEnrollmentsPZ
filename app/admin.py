from django.contrib import admin
from .models import Studenci, Grupy

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class CustomUserAdmin(UserAdmin):
    list_display = ("id", "username", "email", "first_name", "last_name", "is_staff")


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Studenci)
admin.site.register(Grupy)

# Register your models here.
