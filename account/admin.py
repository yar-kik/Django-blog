"""Module for django-admin page"""

from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Class for user profile changes"""

    list_display = ["user", "date_of_birth", "photo", "sex", "phone"]
