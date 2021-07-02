from typing import Type, Optional

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.http import HttpRequest, Http404

from articles.models import Article, Comment


def get_comments_by_id(article_id: Type[int]) -> Comment:
    """
    Return all comments by the article id
    """
    comments = (
        Comment.objects.filter(article_id=article_id)
        .order_by("path")
        .select_related("user", "name__profile", "reply_to")
        .only(
            "article",
            "body",
            "user",
            "created",
            "updated",
            "user__profile__photo",
            "user__username",
            "path",
            "reply_to",
        )
    )
    return comments


def get_all_articles(annotate: bool = True) -> Article:
    """
    Return all articles with predefined fields. If necessary return also count of the comments and likes
    """
    articles = (
        Article.objects.all()
        .select_related("author")
        .prefetch_related()
        .only(
            "title",
            "text",
            "slug",
            "author__username",
            "author__is_staff",
            "date_created",
        )
    )
    if annotate:
        articles = articles.annotate(
            total_comments=Count("comments", distinct=True),
            total_likes=Count("users_like", distinct=True),
        )
    return articles


def get_article_by_slug(
    slug: str, annotate: bool = False
) -> Optional[Article]:
    """
    Return article by the slug
    """
    try:
        article = get_all_articles(annotate).get(slug=slug)
    except ObjectDoesNotExist:
        raise Http404()
    return article


def get_article_by_id(
    article_id: int, annotate: bool = False
) -> Optional[Article]:
    """Return article by the article's id"""
    try:
        article = get_all_articles(annotate).get(id=article_id)
    except ObjectDoesNotExist:
        raise Http404()
    return article


def get_published_articles() -> Article:
    """Return all published article"""
    articles = get_all_articles().filter(status__in=["publish"])
    return articles


def get_moderation_articles() -> Article:
    """Return all articles on moderation"""
    articles = get_all_articles().filter(status__in=["moderation"])
    return articles


def get_draft_articles(request: HttpRequest) -> Article:
    """Return all draft articles"""
    articles = get_all_articles().filter(
        status__in=["draft"], author=request.user
    )
    return articles


def get_parent_comment(comment_id: int) -> Comment:
    """Return parent comment"""
    parent_comment = Comment.objects.only("id", "article", "user", "path").get(
        id=comment_id
    )
    return parent_comment


def get_total_comments(article_id: int) -> int:
    """Return count of the article's total comments"""
    total_comments = Comment.objects.filter(article_id=article_id).count()
    return total_comments


def get_film_articles() -> Article:
    published_articles = get_all_articles().filter(status__in=["publish"])
    articles = published_articles.filter(category="film")
    return articles


def get_anime_articles() -> Article:
    published_articles = get_all_articles().filter(status__in=["publish"])
    articles = published_articles.filter(category="anime")
    return articles


def get_game_articles() -> Article:
    published_articles = get_all_articles().filter(status__in=["publish"])
    articles = published_articles.filter(category="game")
    return articles
