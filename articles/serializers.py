from rest_framework import serializers

from articles.models import Article


class ArticleSerializer(serializers.ModelSerializer):
    total_likes = serializers.SerializerMethodField(read_only=True)
    total_bookmarks = serializers.SerializerMethodField(read_only=True)

    def get_total_likes(self, article: Article) -> int:
        return article.users_like.count()

    def get_total_bookmarks(self, article: Article) -> int:
        return article.users_bookmark.count()

    class Meta:
        model = Article
        fields = ("title", "text", "author", "date_created", "date_updated",
                  "slug", "status", "category", "total_likes",
                  "total_bookmarks")
        read_only_fields = ("author", "total_likes", "total_bookmarks")
        lookup_field = 'slug'
