from django.contrib import admin
from .models import Film, Anime, Game

@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'actors', 'directors')
