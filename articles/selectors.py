from articles.models import Article, Comment


def get_comments(article: Article) -> Comment:
    comments = article.comments.order_by('path').\
        select_related('name', 'name__profile').only('article', 'body', 'name', 'created', 'updated',
                                                     'name__profile__photo', 'name__username', 'path')
    return comments


def get_article(slug: str) -> Article:
    article = Article.objects.filter(slug=slug). \
        select_related('author').only('title', 'text', 'slug', 'author__username',
                                      'author__is_staff', 'date_created', ).get()
    return article


def get_parent_comment(comment_id: int) -> Comment:
    parent_comment = Comment.objects.only('id', 'article', 'name').get(id=comment_id)
    return parent_comment
