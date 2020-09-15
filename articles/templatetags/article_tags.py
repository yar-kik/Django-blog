from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

from ..models import Article

register = template.Library()


@register.simple_tag
def total_articles():
    return Article.objects.count()


@register.inclusion_tag('articles/post/latest_articles.html')
def show_latest_articles(count=5):
    latest_articles = Article.objects.order_by('-date_created')[:count]
    return {'latest_articles': latest_articles}


@register.simple_tag
def get_most_commented_articles(count=5):
    return Article.objects.annotate(total_comments=Count('comments')).\
               order_by('-total_comments')[:count]


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
