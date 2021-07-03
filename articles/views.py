import logging
import redis
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, \
    RetrieveUpdateDestroyAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Article, Comment
from .selectors import (
    get_moderation_articles,
    get_published_articles,
    get_draft_articles,
    get_film_articles,
    get_anime_articles,
    get_game_articles,
)
from .serializers import ArticleSerializer, CommentSerializer
from .services import (
    paginate_articles,
)

logger = logging.getLogger(__name__)

r = redis.StrictRedis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB
)


class ListCommentApiView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = "article__id"
    lookup_url_kwarg = "article_id"

    def create(self, request: Request, *args, **kwargs):
        comment = request.data.get("comment")
        serializer = self.serializer_class(data=comment)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user,
                            article_id=kwargs.get("article_id"))
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SingleCommentApiView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_url_kwarg = "comment_id"


class ListArticleApiView(ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def create(self, request, *args, **kwargs):
        article = request.data.get("article")
        serializer = self.serializer_class(data=article)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SingleArticleApiView(RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_url_kwarg = "article_id"
