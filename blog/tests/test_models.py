"""Module to test blog models"""

from django.test import TestCase

from authentication.models import User
from blog.models import Article, Comment


class TestArticleModel(TestCase):
    """Test article database model"""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="user", email="email@mail.com", password="password"
        )
        cls.article = Article.objects.create(
            title="First article", author=cls.user, body="Some text"
        )

    def test_str(self):
        """Testing article model string representation"""

        self.assertEqual(str(self.article), "<Article> First article (user)")


class TestCommentModel(TestCase):
    """Test comment database model"""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="user", email="email@mail.com", password="password"
        )
        cls.article = Article.objects.create(
            title="First article",
            author=cls.user,
            body="Some text",
            status="publish",
        )
        cls.article2 = Article.objects.create(
            title="Second article",
            author=cls.user,
            body="Another text",
            status="draft",
        )
        cls.comment = Comment.objects.create(
            article=cls.article, author=cls.user, body="Some comment"
        )

    def test_str(self):
        """Testing comment model string representation"""

        self.assertEqual(str(self.comment), "<Comment> First article (user)")

    def test_published(self):
        """Testing article model manager"""

        self.assertNotIn(self.article2, Article.published.all())
