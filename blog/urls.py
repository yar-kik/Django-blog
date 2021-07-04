"""Module for blog app urls"""

from django.urls import path

from .views import (
    SingleArticleApiView,
    ListArticleApiView,
    ListCommentApiView,
    SingleCommentApiView,
    ArticleLikeApiView,
    CommentLikeApiView,
)

# pylint: disable=invalid-name
app_name = "blog"
urlpatterns = [
    path("articles/", ListArticleApiView.as_view()),
    path("articles/<int:article_id>/", SingleArticleApiView.as_view()),
    path("articles/<int:article_id>/like/", ArticleLikeApiView.as_view()),
    path("articles/<int:article_id>/comments/", ListCommentApiView.as_view()),
    path("comments/<int:comment_id>/", SingleCommentApiView.as_view()),
    path("comments/<int:comment_id>/like/", CommentLikeApiView.as_view())
]
