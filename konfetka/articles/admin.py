from django.contrib import admin
from .models import Article, Comment


@admin.register(Article)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date_created', 'date_updated')
    list_filter = ('date_created', 'date_updated')
    search_fields = ('title', 'author')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'article', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')
