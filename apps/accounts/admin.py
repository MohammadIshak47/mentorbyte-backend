from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ("email", "username", "full_name", "is_staff", "created_at")
    search_fields = ("email", "username", "full_name")
    ordering = ("-created_at",)
