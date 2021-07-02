"""Module for django-admin page"""

from django.contrib import admin

from authentication.models import User


@admin.register(User)
class ProfileAdmin(admin.ModelAdmin):
    """Class for user profile changes"""

    list_display = ["username", "email", "is_staff", "is_superuser", "last_login", "last_request"]
