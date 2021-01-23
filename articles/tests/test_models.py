from django.contrib.auth.models import User
from django.test import TestCase

from articles.models import Article, Comment


class TestArticleModel(TestCase):
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


class TestCommentModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='user',
            password='pass'
        )
        cls.article = Article.objects.create(
            title="First article",
            author=cls.user,
            text='Some text',
            status='publish')
        cls.article2 = Article.objects.create(
            title='Second article',
            author=cls.user,
            text='Another text',
            status='draft'
        )
        cls.comment = Comment.objects.create(
            article=cls.article,
            name=cls.user,
            body='Some comment'
        )

    def test_str(self):
        self.assertEqual(str(self.comment),
                         "Comment by user on First article")

    def test_published(self):
        self.assertNotIn(self.article2, Article.published.all())

    def test_comment_path(self):
        self.assertIn(self.comment.id, self.comment.path)

    def test_get_offset(self):
        self.assertEqual(self.comment.get_offset(), 1)
        self.comment.path = [i for i in range(8)]
        self.assertEqual(self.comment.get_offset(), 5)
