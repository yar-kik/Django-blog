"""Module for blog app serializers"""

from rest_framework import serializers

from blog.models import Article, Comment


class ArticleSerializer(serializers.ModelSerializer):
    """Article serializer/deserializer"""

    total_likes = serializers.SerializerMethodField(read_only=True)
    total_bookmarks = serializers.SerializerMethodField(read_only=True)
    total_comments = serializers.SerializerMethodField(read_only=True)

    # pylint: disable=no-self-use
    def get_total_comments(self, article: Article) -> int:
        """Return total number of the article comments"""
        return article.comments.count()

    def get_total_likes(self, article: Article) -> int:
        """Return total number of the article likes"""
        return article.users_like.count()

    def get_total_bookmarks(self, article: Article) -> int:
        """Return total number of the article bookmarks"""
        return article.users_bookmark.count()

    # pylint: disable=missing-class-docstring
    class Meta:
        model = Article
        fields = (
            "id",
            "title",
            "text",
            "author",
            "date_created",
            "date_updated",
            "status",
            "category",
            "total_likes",
            "total_comments",
            "total_bookmarks",
        )
        read_only_fields = (
            "id",
            "author",
            "total_likes",
            "total_bookmarks",
            "total_comments",
            "date_created",
            "date_updated",
        )


class CommentSerializer(serializers.ModelSerializer):
    """Comment serializer/deserializer"""

    total_likes = serializers.SerializerMethodField(read_only=True)

    # pylint: disable=no-self-use
    def get_total_likes(self, comment: Comment) -> int:
        """Return total number of the comments likes"""
        return comment.users_like.count()

    # pylint: disable=missing-class-docstring
    class Meta:
        model = Comment
        fields = (
            "id",
            "article_id",
            "user",
            "body",
            "created",
            "updated",
            "active",
            "total_likes",
        )
        read_only_fields = (
            "id",
            "article_id",
            "user",
            "updated",
            "created",
            "total_likes",
        )
        lookup_field = "article__id"
