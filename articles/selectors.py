from typing import Type

from django.db.models import Count
from django.http import HttpRequest

from articles.models import Article, Comment


def get_comments_by_id(article_id: Type[int]) -> Comment:
    comments = Comment.objects.filter(article_id=article_id).order_by('path').\
        select_related('name', 'name__profile', 'reply_to').only('article', 'body', 'name', 'created', 'updated',
                                                                 'name__profile__photo', 'name__username', 'path',
                                                                 'reply_to')
    return comments


def get_all_articles(annotate: bool = True) -> Article:
    articles = Article.objects.all().select_related('author').prefetch_related().\
        only('title', 'text', 'slug', 'author__username', 'author__is_staff', 'date_created')
    if annotate:
        articles = articles.annotate(total_comments=Count('comments', distinct=True),
                                     total_likes=Count('users_like', distinct=True))
    return articles


def get_article_by_slug(slug: str, annotate: bool = False) -> Article:
    article = get_all_articles(annotate).get(slug=slug)
    return article


def get_article_by_id(article_id: int, annotate: bool = False) -> Article:
    article = get_all_articles(annotate).get(id=article_id)
    return article


def get_published_articles() -> Article:
    articles = get_all_articles().filter(status__in=['publish'])
    return articles


def get_moderation_articles() -> Article:
    articles = get_all_articles().filter(status__in=['moderation'])
    return articles


def get_draft_articles(request: HttpRequest) -> Article:
    articles = get_all_articles().filter(status__in=['draft'], author=request.user)
    return articles


def get_parent_comment(comment_id: int) -> Comment:
    parent_comment = Comment.objects.only('id', 'article', 'name', 'path').get(id=comment_id)
    return parent_comment


def get_total_comments(article_id: int) -> int:
    total_comments = Comment.objects.filter(article_id=article_id).count()
    return total_comments
