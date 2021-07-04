"""Module for the blog app models"""

from django.conf import settings
from django.db import models

from authentication.models import User


class PublishedManager(models.Manager):
    """Manager of a published articles"""

    def get_queryset(self):
        """Return queryset of a published articles"""
        return super().get_queryset().filter(status="publish")


CATEGORIES = [("film", "Film"), ("game", "Game"), ("anime", "Anime")]
STATUS_CHOICES = [
    ("draft", "Drafted"),
    ("moderation", "On moderation"),
    ("publish", "Published"),
]


# pylint: disable=no-member
class Article(models.Model):
    """Article database model"""

    category = models.CharField(
        max_length=16,
        choices=CATEGORIES,
        default="film",
        blank=True,
    )
    title = models.CharField(max_length=100, unique=True)
    author: User = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    body = models.TextField(max_length=20000)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    published = PublishedManager()

    status = models.CharField(
        max_length=16,
        choices=STATUS_CHOICES,
        default="draft",
        blank=True,
    )

    # pylint: disable=missing-class-docstring
    class Meta:
        ordering = ("-created",)
        permissions = [
            ("can_moderate_article", "Can moderate article"),
            ("can_draft_article", "Can create draft article"),
        ]

    def __str__(self) -> str:
        return f"<Article> {self.title} ({self.author.username})"


class Comment(models.Model):
    """Comment database model"""

    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="comments"
    )
    author: User = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    objects = models.Manager()
    body = models.TextField(max_length=2000, verbose_name="")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    reply_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reply",
        null=True,
        blank=True,
    )

    # pylint: disable=missing-class-docstring
    class Meta:
        ordering = ("-created",)

    def __str__(self) -> str:
        return f"<Comment> {self.article.title} ({self.author.username})"


class ArticleLike(models.Model):
    """Article like database model"""

    article: Article = models.ForeignKey(
        Article, related_name="likes", on_delete=models.CASCADE
    )
    user: User = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="article_likes",
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return f"<ArticleLike> {self.article.title} ({self.user.username})"


class CommentLike(models.Model):
    """Comment like database model"""

    comment: Comment = models.ForeignKey(
        Comment, related_name="likes", on_delete=models.CASCADE
    )
    user: User = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="comment_likes",
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return f"<CommentLike> {self.user.username} ({self.created})"


class ArticleBookmark(models.Model):
    """Article bookmark database model"""

    article: Article = models.ForeignKey(
        Article, related_name="bookmarks", on_delete=models.CASCADE
    )
    user: User = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="article_bookmarks",
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return f"<ArticleBookmark> {self.article.title} ({self.user.username})"
