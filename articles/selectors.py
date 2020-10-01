from django.db.models import Count

from articles.models import Article, Comment


def get_comments_by_instance(article: Article) -> Comment:
    comments = article.comments.order_by('path').\
        select_related('name', 'name__profile').only('article', 'body', 'name', 'created', 'updated',
                                                     'name__profile__photo', 'name__username', 'path',
                                                     'reply_to')
    return comments


def get_comments_by_id(article_id: int) -> Comment:
    comments = Comment.objects.filter(article_id=article_id).order_by('path').\
        select_related('name', 'name__profile').only('article', 'body', 'name', 'created', 'updated',
                                                     'name__profile__photo', 'name__username', 'path',
                                                     'reply_to')
    return comments


def get_article(slug: str) -> Article:
    article = Article.objects.filter(slug=slug). \
        select_related('author').only('title', 'text', 'slug', 'author__username',
                                      'author__is_staff', 'date_created').get()
    return article


def get_all_articles() -> Article:
    articles = Article.objects.all().select_related('author').\
        only('title', 'text', 'slug', 'author__username', 'author__is_staff', 'date_created').\
        annotate(total_comments=Count('comments', distinct=True), total_likes=Count('users_like', distinct=True))
    return articles


def get_published_articles() -> Article:
    articles = get_all_articles().filter(status__in=['publish'])
    return articles


def get_moderation_articles() -> Article:
    articles = get_all_articles().filter(status__in=['moderation'])
    return articles


def get_draft_articles(request) -> Article:
    articles = get_all_articles().filter(status__in=['draft'], author=request.user)
    return articles


def get_parent_comment(comment_id: int) -> Comment:
    parent_comment = Comment.objects.only('id', 'article', 'name').get(id=comment_id)
    return parent_comment


def get_total_comments(article_id: int) -> int:
    total_comments = Comment.objects.filter(article_id=article_id).count()
    return total_comments
