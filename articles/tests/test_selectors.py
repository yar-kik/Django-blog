from django.contrib.auth.models import User
from django.http import Http404
from django.test import TestCase

from articles.forms import CommentForm
from articles.models import Article, Comment
from articles import selectors


class TestArticleServices(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_superuser(
            username='admin',
            email='mail@mail.com',
            password='pass'
        )
        cls.article = Article.objects.create(
            title="First article",
            author=cls.admin,
            text='Some text',
            status='publish')
        for i in range(1, 11):
            Comment.objects.create(
                name=cls.admin,
                body=f"Test #{i}",
                article=cls.article
            )

    def test_get_article_by_slug(self):
        article = selectors.get_article_by_slug("first-article")
        self.assertEqual(article, self.article)
        with self.assertRaises(Http404):
            selectors.get_article_by_slug('fake-slug')

    def test_get_article_by_id(self):
        article = selectors.get_article_by_id(self.article.id)
        self.assertEqual(article, self.article)
        with self.assertRaises(Http404):
            selectors.get_article_by_id(100)

    def test_get_total_comments(self):
        number_of_comments = selectors.get_total_comments(self.article.id)
        self.assertEqual(number_of_comments, 10)