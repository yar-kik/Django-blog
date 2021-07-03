from rest_framework import serializers

from blog.models import Article, Comment


class ArticleSerializer(serializers.ModelSerializer):
    total_likes = serializers.SerializerMethodField(read_only=True)
    total_bookmarks = serializers.SerializerMethodField(read_only=True)
    total_comments = serializers.SerializerMethodField(read_only=True)

    def get_total_comments(self, article: Article) -> int:
        return article.comments.count()

    def get_total_likes(self, article: Article) -> int:
        return article.users_like.count()

    def get_total_bookmarks(self, article: Article) -> int:
        return article.users_bookmark.count()

    class Meta:
        model = Article
        fields = (
            "id", "title", "text", "author", "date_created", "date_updated",
            "status", "category", "total_likes", "total_comments",
            "total_bookmarks")
        read_only_fields = (
            "id", "author", "total_likes", "total_bookmarks", "total_comments",
            "date_created", "date_updated")


class CommentSerializer(serializers.ModelSerializer):
    total_likes = serializers.SerializerMethodField(read_only=True)

    def get_total_likes(self, comment: Comment) -> int:
        return comment.users_like.count()

    class Meta:
        model = Comment
        fields = (
            "id", "article_id", "user", "body", "created", "updated", "active",
            "total_likes")
        read_only_fields = (
            "id", "article_id", "user", "updated", "created", "total_likes")
        lookup_field = "article__id"
