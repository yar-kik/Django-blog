from django.contrib.auth.models import User
from django.test import TestCase

from articles.models import Article, Comment


class TestArticle(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='user',
            password='pass'
        )
        cls.article = Article.objects.create(
            title="First article",
            author=cls.user,
            text='Some text')

    def test_str(self):
        self.assertEqual(str(self.article), "First article")

    def test_get_absolute_url(self):
        self.assertEqual(self.article.get_absolute_url(),
                         "/articles/first-article/")


class TestComment(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='user',
            password='pass'
        )
        cls.article = Article.objects.create(
            title="First article",
            author=cls.user,
            text='Some text')
        cls.comment = Comment.objects.create(
            article=cls.article,
            name=cls.user,
            body='Some comment'
        )

    def test_str(self):
        self.assertEqual(str(self.comment),
                         "Comment by user on First article")

    def test_comment_path(self):
        self.assertIn(1, self.comment.path)

    def test_get_offset(self):
        self.assertEqual(self.comment.get_offset(), 1)

    def test_get_col(self):
        self.assertEqual(self.comment.get_col(), 23)
