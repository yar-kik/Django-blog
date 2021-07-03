"""Module to admin blog app"""

from django.contrib import admin
from .models import Article, Comment


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """Article instances administration"""

    list_display = ("title", "author", "date_created", "date_updated")
    list_filter = ("date_created", "date_updated")
    search_fields = ("title", "author")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Comment instances administration"""

    list_display = ("user", "article", "body", "created", "updated")
    list_filter = ("active", "created", "updated")
    search_fields = ("user", "body")
