from django.contrib.auth.models import User
from django.test import TestCase

from articles.forms import CommentForm
from articles.models import Article, Comment
from articles import services


class TestArticleServices(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="user", password="pass", email="e@mail.com"
        )
        cls.article = Article.objects.create(
            title="First article",
            author=cls.user,
            text="Some text",
            status="publish",
        )
        cls.admin = User.objects.create_superuser(
            username="admin", email="mail@mail.com", password="pass"
        )
        cls.comment = Comment.objects.create(
            name=cls.user, body="Test", article=cls.article
        )
        cls.user2 = User.objects.create_user(
            username="user2", password="pass", email="e2@mail.com"
        )
        for i in range(2, 20):
            Comment.objects.create(
                name=cls.user, body="Test", article=cls.article
            )

        for i in range(2, 10):
            Article.objects.create(
                title=f"Article #{i}",
                author=cls.user,
                text="Some text",
                status="publish",
            )

    def setUp(self) -> None:
        self.comment_form = CommentForm(data={"body": "some comment"})
        self.client.login(username="user", password="pass")
        self.request = self.client.get("/article/").wsgi_request

    def test_create_reply_form(self):
        new_comment = services.create_reply_form(
            self.request, self.comment_form, self.comment
        )
        new_comment.save()
        self.assertEqual(new_comment.name, self.user)
        self.assertEqual(new_comment.reply_to, self.comment.user)
        self.assertEqual(new_comment.path, [self.comment.id, new_comment.id])

    def test_create_comment_form(self):
        new_comment = services.create_comment_form(
            self.request, self.comment_form, self.article.id
        )
        new_comment.save()
        self.assertEqual(new_comment.user, self.user)
        self.assertEqual(new_comment.article_id, self.article.id)

    def test_is_author(self):
        # Check if true user is author of a comment
        self.assertTrue(services.is_author(self.request, self.comment))
        # Check if anonymous user is author of a comment
        self.client.logout()
        self.request = self.client.get("/article/").wsgi_request
        self.assertFalse(services.is_author(self.request, self.comment))
        # Check if fake user is author of a comment
        self.client.login(username="user2", password="pass")
        self.request = self.client.get("/article/").wsgi_request
        self.assertFalse(services.is_author(self.request, self.comment))
        # Check if admin or staff is author of a comment
        self.client.login(username="user2", password="pass")
        self.request = self.client.get("/article/").wsgi_request

    def test_paginate_articles(self):
        # Check if page not defined
        object_list = Article.objects.all()
        articles = services.paginate_articles(self.request, object_list)
        self.assertEqual(len(articles), 6)
        # Check if page is integer within a paginated QuerySet
        self.request = self.client.get(
            "/article/", data={"page": 2}
        ).wsgi_request
        articles = services.paginate_articles(self.request, object_list)
        self.assertEqual(len(articles), 3)
        # Check if page is integer outside a paginated QuerySet
        self.request = self.client.get(
            "/article/", data={"page": 3}
        ).wsgi_request
        articles = services.paginate_articles(self.request, object_list)
        self.assertEqual(len(articles), 3)

    def test_paginate_comments(self):
        # Check if page not defined
        object_list = Comment.objects.all()
        comments = services.paginate_comments(self.request, object_list)
        self.assertEqual(len(comments), 16)
        # Check if page is integer within a paginated QuerySet
        self.request = self.client.get(
            "/article/", data={"page": 2}
        ).wsgi_request
        comments = services.paginate_comments(self.request, object_list)
        self.assertEqual(len(comments), 3)
        # Check if page is integer outside a paginated QuerySet
        self.request = self.client.get(
            "/article/", data={"page": 3}
        ).wsgi_request
        comments = services.paginate_comments(self.request, object_list)
        self.assertIsNone(comments)
