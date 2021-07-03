"""Module for blog app sitemaps"""

from django.contrib.sitemaps import Sitemap
from .models import Article


class ArticleSitemap(Sitemap):
    """Article sitemap"""

    changefreq = "weekly"
    priority = 0.9

    # pylint: disable=no-self-use
    def items(self):
        return Article.objects.all()

    def lastmod(self, obj):
        return obj.date_updated
