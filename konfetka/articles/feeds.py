from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords

from articles.models import Article


class LatestArticlesFeed(Feed):
    title = 'My Blog'
    link = '/blog/'
    description = 'New articles of my blog'

    def items(self):
        return Article.objects.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.text, 30)
