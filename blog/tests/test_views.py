"""Module to test blog app views"""

import unittest

from rest_framework.response import Response
from rest_framework.test import APITestCase

from authentication.models import User
from blog.models import Article, Comment


class TestListArticleApiView(APITestCase):
    """Test to create article and get a list of all articles"""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="user", email="email@mail.com", password="password"
        )

    def test_create_article_if_unauthorized(self):
        """Testing article creating if user if not authorized"""

        response = self.client.post("/blog/articles/")
        self.assertEqual(response.status_code, 403)

    def test_create_article_if_empty_input(self):
        """Testing article creating if input is empty"""

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.user.token)
        response = self.client.post("/blog/articles/")
        self.assertEqual(response.status_code, 400)

    def test_create_article_if_invalid_data(self):
        """Testing article creating if data is invalid"""

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.user.token)
        response = self.client.post(
            "/blog/articles/", data={"article": {"title": ""}}
        )
        self.assertEqual(response.status_code, 400)

    def test_create_article_successfully(self):
        """Testing article successful creation"""
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.user.token)
        response = self.client.post(
            "/blog/articles/",
            data={
                "article": {"title": "Article title", "body": "Article text"}
            },
        )
        self.assertEqual(response.status_code, 201)
        article = Article.objects.first()
        self.assertEqual(article.title, "Article title")

    def test_get_articles_list(self):
        """Testing get list of all articles"""
        Article.objects.create(
            title="Article title", body="Article text", author=self.user
        )
        response: Response = self.client.get("/blog/articles/")
        self.assertEqual(response.status_code, 200)
        posts = response.json()
        self.assertEqual(posts[0]["title"], "Article title")


class TestArticleApiView(APITestCase):
    """Test single article get, update and delete functions"""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="user", email="email@mail.com", password="password"
        )
        cls.user2 = User.objects.create_user(
            username="user2", email="email2@mail.com", password="password"
        )

    def test_get_article_if_not_exist(self):
        """Testing get a single article if it doesn't exist"""
        response = self.client.get("/blog/articles/1/")
        self.assertEqual(response.status_code, 404)

    def test_get_article_successfully(self):
        """Testing get successfully a single article"""
        Article.objects.create(
            title="Article title", body="Article text", author=self.user
        )
        response = self.client.get("/blog/articles/1/")
        self.assertEqual(response.status_code, 200)

    def test_update_article_if_not_authorized(self):
        """Testing update article if user isn't authorized"""
        response = self.client.patch("/blog/articles/1/")
        self.assertEqual(response.status_code, 403)

    def test_update_article_if_not_exists(self):
        """Testing update article if it doesn't exist"""
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.user.token)
        response = self.client.patch("/blog/articles/1/")
        self.assertEqual(response.status_code, 404)

    def test_update_article_if_not_author(self):
        """Testing update article if user isn't author of it"""
        Article.objects.create(
            title="Article title", body="Article text", author=self.user2
        )
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.user.token)
        response = self.client.patch("/blog/articles/1/")
        self.assertEqual(response.status_code, 403)

    def test_update_article_successfully(self):
        """Testing successfully update article"""
        Article.objects.create(
            title="Article title", body="Article text", author=self.user
        )
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.user.token)
        response = self.client.patch(
            "/blog/articles/1/", data={"title": "Updated title"}
        )
        self.assertEqual(response.status_code, 200)
        article = Article.objects.first()
        self.assertEqual(article.title, "Updated title")

    def test_delete_article_if_not_exists(self):
        """Testing delete article if it doesn't exist"""
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.user.token)
        response = self.client.delete("/blog/articles/1/")
        self.assertEqual(response.status_code, 404)

    def test_delete_article_if_not_authorized(self):
        """Testing delete article if user isn't authorized"""
        Article.objects.create(
            title="Article title", body="Article text", author=self.user
        )
        response = self.client.delete("/blog/articles/1/")
        self.assertEqual(response.status_code, 403)

    def test_delete_article_if_not_author(self):
        """Testing delete article if user isn't author"""
        Article.objects.create(
            title="Article title", body="Article text", author=self.user2
        )
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.user.token)
        response = self.client.delete("/blog/articles/1/")
        self.assertEqual(response.status_code, 403)

    def test_delete_article_successfully(self):
        """Testing successfully delete article"""
        Article.objects.create(
            title="Article title", body="Article text", author=self.user
        )
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.user.token)
        response = self.client.delete("/blog/articles/1/")
        self.assertEqual(response.status_code, 204)
        article = Article.objects.all()
        self.assertEqual(article.count(), 0)


class TestCommentApiView(APITestCase):
    """Test single comment get, update and delete functions"""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="user", email="email@mail.com", password="password"
        )
        cls.user2 = User.objects.create_user(
            username="user2", email="email2@mail.com", password="password"
        )
        cls.article = Article.objects.create(
            author=cls.user, title="Article title", body="Article text"
        )

    def test_get_comment_if_not_exist(self):
        """Testing get a single article if it doesn't exist"""
        response = self.client.get("/blog/comments/1/")
        self.assertEqual(response.status_code, 404)

    def test_get_comment_successfully(self):
        """Testing get successfully a single comment"""
        Comment.objects.create(
            article=self.article, body="Comment text", author=self.user
        )
        response = self.client.get("/blog/comments/1/")
        self.assertEqual(response.status_code, 200)

    def test_update_comment_if_not_authorized(self):
        """Testing update comment if user isn't authorized"""
        response = self.client.patch("/blog/comments/1/")
        self.assertEqual(response.status_code, 403)

    def test_update_comment_if_not_exists(self):
        """Testing update comment if it doesn't exist"""
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.user.token)
        response = self.client.patch("/blog/comments/1/")
        self.assertEqual(response.status_code, 404)

    def test_update_comment_if_not_author(self):
        """Testing update comment if user isn't author of it"""
        Comment.objects.create(
            article=self.article, body="Comment text", author=self.user2
        )
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.user.token)
        response = self.client.patch("/blog/comments/1/")
        self.assertEqual(response.status_code, 403)

    def test_update_comment_successfully(self):
        """Testing successfully update comment"""
        Comment.objects.create(
            article=self.article, body="Comment text", author=self.user
        )
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.user.token)
        response = self.client.patch(
            "/blog/comments/1/", data={"body": "Updated text"}
        )
        self.assertEqual(response.status_code, 200)
        comment = Comment.objects.first()
        self.assertEqual(comment.body, "Updated text")

    def test_delete_comment_if_not_exists(self):
        """Testing delete comment if it doesn't exist"""
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.user.token)
        response = self.client.delete("/blog/comments/1/")
        self.assertEqual(response.status_code, 404)

    def test_delete_comment_if_not_authorized(self):
        """Testing delete comment if user isn't authorized"""
        Comment.objects.create(
            article=self.article, body="Comment text", author=self.user
        )
        response = self.client.delete("/blog/comments/1/")
        self.assertEqual(response.status_code, 403)

    def test_delete_comment_if_not_author(self):
        """Testing delete comment if user isn't author"""
        Comment.objects.create(
            article=self.article, body="Comment text", author=self.user2
        )
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.user.token)
        response = self.client.delete("/blog/comments/1/")
        self.assertEqual(response.status_code, 403)

    def test_delete_comment_successfully(self):
        """Testing successfully delete comment"""
        Comment.objects.create(
            article=self.article, body="Article text", author=self.user
        )
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.user.token)
        response = self.client.delete("/blog/comments/1/")
        self.assertEqual(response.status_code, 204)
        comments = self.article.comments.all()
        self.assertEqual(comments.count(), 0)


class TestArticleLikeApiView(APITestCase):
    """Test article like"""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="user", email="email@mail.com", password="password"
        )
        cls.article = Article.objects.create(
            title="Article title", body="Article text", author=cls.user
        )

    def test_like_if_not_authorized(self):
        """Testing like article if user isn't authorized"""
        response = self.client.get("/blog/articles/1/like/")
        self.assertEqual(response.status_code, 403)

    def test_like_if_article_not_exists(self):
        """Testing like article if it doesn't exist"""
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.user.token)
        response = self.client.get("/blog/articles/2/like/")
        self.assertEqual(response.status_code, 404)

    def test_like_if_article_not_liked_yet(self):
        """Testing like article if user doesn't like it yet"""
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.user.token)
        response = self.client.get("/blog/articles/1/like/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["detail"], "Article was liked")

    def test_like_if_article_was_liked(self):
        """Testing like article if user liked it before"""
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.user.token)
        self.client.get("/blog/articles/1/like/")
        response = self.client.get("/blog/articles/1/like/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["detail"], "Article was unliked")


class TestCommentLikeApiView(APITestCase):
    """Test comment like"""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="user", email="email@mail.com", password="password"
        )
        cls.article = Article.objects.create(
            title="Article title", body="Article text", author=cls.user
        )
        cls.comment = Comment.objects.create(
            article=cls.article, author=cls.user, body="Comment text"
        )

    def test_like_if_not_authorized(self):
        """Testing like comment if user isn't authorized"""
        response = self.client.get("/blog/comments/1/like/")
        self.assertEqual(response.status_code, 403)

    def test_like_if_comment_not_exists(self):
        """Testing like comment if it doesn't exist"""
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.user.token)
        response = self.client.get("/blog/comments/2/like/")
        self.assertEqual(response.status_code, 404)

    def test_like_if_comment_not_liked_yet(self):
        """Testing like comment if user doesn't like it yet"""
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.user.token)
        response = self.client.get("/blog/comments/1/like/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["detail"], "Comment was liked")

    def test_like_if_comment_was_liked(self):
        """Testing like comment if user liked it before"""
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.user.token)
        self.client.get("/blog/comments/1/like/")
        response = self.client.get("/blog/comments/1/like/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["detail"], "Comment was unliked")
