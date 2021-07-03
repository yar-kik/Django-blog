"""Module to admin archive app"""

from django.contrib import admin
from .models import Film


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    """Administration of the film instances"""

    list_display = ("title", "release_date")
