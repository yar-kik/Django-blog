"""Module for the blog app models"""

from django.conf import settings
from django.db import models

from archives.models import InfoBase


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


class Article(models.Model):
    """Article database model"""

    category = models.CharField(
        max_length=16,
        choices=CATEGORIES,
        default="film",
        verbose_name="категорія",
        blank=True,
    )
    related_item = models.ForeignKey(
        InfoBase, on_delete=models.CASCADE, null=True, blank=True
    )
    title = models.CharField(
        max_length=100, verbose_name="назва статті", unique=True
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="автор",
    )
    text = models.TextField(max_length=20000, verbose_name="текст")
    date_created = models.DateTimeField(
        auto_now_add=True, verbose_name="дата створення"
    )
    date_updated = models.DateTimeField(
        auto_now=True, verbose_name="дата редагування"
    )
    objects = models.Manager()
    published = PublishedManager()
    users_like = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="articles_liked", blank=True
    )
    users_bookmark = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="articles_bookmarked",
        blank=True,
    )
    status = models.CharField(
        max_length=16,
        choices=STATUS_CHOICES,
        default="draft",
        verbose_name="статус",
        blank=True,
    )

    # pylint: disable=missing-class-docstring
    class Meta:
        ordering = ("-date_created",)
        permissions = [
            ("can_moderate_article", "Може одобрювати статті"),
            ("can_draft_article", "Може створювати чернетку статті"),
        ]

    def __str__(self) -> str:
        return str(self.title)


class Comment(models.Model):
    """Comment database model"""

    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="comments"
    )
    user = models.ForeignKey(
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
    users_like = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="comments_liked"
    )

    # pylint: disable=missing-class-docstring
    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return f"Comment by {self.user} on {self.article}"
