"""Module for blog app controllers (views)"""

import logging
import redis
from django.conf import settings
from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Article, Comment
from .permissions import IsAuthor
from .serializers import ArticleSerializer, CommentSerializer

logger = logging.getLogger(__name__)

r = redis.StrictRedis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB
)


# pylint: disable=too-many-ancestors
class ListCommentApiView(ListCreateAPIView):
    """Endpoint to create a new comment or to get a list of the certain article
    comment"""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = "article__id"
    lookup_url_kwarg = "article_id"
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request: Request, *args, **kwargs):
        comment = request.data.get("comment")
        serializer = self.serializer_class(data=comment)
        if serializer.is_valid(raise_exception=True):
            serializer.save(
                user=request.user, article_id=kwargs.get("article_id")
            )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SingleCommentApiView(RetrieveUpdateDestroyAPIView):
    """Endpoint to get, update or delete a single comment by comment id"""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_url_kwarg = "comment_id"
    permission_classes = IsAuthenticatedOrReadOnly & IsAuthor


class ListArticleApiView(ListCreateAPIView):
    """Endpoint to get create a new article or get a list of all articles"""

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request, *args, **kwargs):
        article = request.data.get("article")
        serializer = self.serializer_class(data=article)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SingleArticleApiView(RetrieveUpdateDestroyAPIView):
    """Endpoint to get, update or delete a single article by article id"""

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_url_kwarg = "article_id"
    permission_classes = [IsAuthenticatedOrReadOnly & IsAuthor]
