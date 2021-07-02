from django.urls import path

from . import views
from .views import SingleArticleApiView, ListArticleApiView

app_name = "articles"
urlpatterns = [
    path("", ListArticleApiView.as_view()),
    path("<slug:slug>/", SingleArticleApiView.as_view()),
    path("moderation_list/", views.moderation_list, name="moderation_list"),
    path("draft_list/", views.draft_list, name="draft_list"),
    path("like_article/", views.article_like, name="like_article"),
    path("film_articles/", views.film_articles_list, name="film_articles"),
    path("anime_articles/", views.anime_articles_list, name="anime_articles"),
    path("game_articles/", views.game_articles_list, name="game_articles"),
    path("search/", views.article_search, name="article_search"),
    path("bookmark_article/", views.bookmark_article, name="bookmark_article"),
    path(
        "<int:comment_id>/update_comment/",
        views.edit_comment,
        name="edit_comment",
    ),
    path(
        "<int:comment_id>/delete_comment/",
        views.delete_comment,
        name="delete_comment",
    ),
    path(
        "<int:comment_id>/reply_comment/",
        views.reply_comment,
        name="reply_comment",
    ),
    path(
        "<int:article_id>/create_comment/",
        views.create_comment,
        name="create_comment",
    ),
    path(
        "<int:article_id>/all_comments/",
        views.comments_list,
        name="all_comments",
    ),

]
