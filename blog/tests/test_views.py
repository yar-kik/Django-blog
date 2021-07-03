"""Module to test blog app views"""

import unittest

from rest_framework.response import Response
from rest_framework.test import APITestCase

from authentication.models import User
from blog.models import Article


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

    def test_create_post_successfully(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.user.token)
        response = self.client.post(
            "/blog/articles/",
            data={
                "article": {"title": "Article title", "text": "Article text"}
            },
        )
        self.assertEqual(response.status_code, 201)
        article = Article.objects.first()
        self.assertEqual(article.title, "Article title")

    def test_get_posts_list(self):
        Article.objects.create(
            title="Article title", text="Article text", author=self.user
        )
        response: Response = self.client.get("/blog/articles/")
        self.assertEqual(response.status_code, 200)
        posts = response.json()
        self.assertEqual(posts[0]["title"], "Article title")


class TestArticleApiView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="user", email="email@mail.com", password="password"
        )
        cls.user2 = User.objects.create_user(
            username="user2", email="email2@mail.com", password="password"
        )

    def test_get_post_if_not_exist(self):
        response = self.client.get("/blog/articles/1/")
        self.assertEqual(response.status_code, 404)

    def test_get_post_successfully(self):
        Article.objects.create(
            title="Article title", text="Article text", author=self.user
        )
        response = self.client.get("/blog/articles/1/")
        self.assertEqual(response.status_code, 200)

    def test_update_post_if_not_authorized(self):
        response = self.client.patch("/blog/articles/1/")
        self.assertEqual(response.status_code, 403)

    def test_update_post_if_not_exists(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.user.token)
        response = self.client.patch("/blog/articles/1/")
        self.assertEqual(response.status_code, 404)

    def test_update_post_if_not_author(self):
        Article.objects.create(
            title="Article title", text="Article text", author=self.user2
        )
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.user.token)
        response = self.client.patch("/blog/articles/1/")
        self.assertEqual(response.status_code, 403)

    def test_update_post_successfully(self):
        Article.objects.create(
            title="Article title", text="Article text", author=self.user
        )
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.user.token)
        response = self.client.patch(
            "/blog/articles/1/", data={"title": "Updated title"}
        )
        self.assertEqual(response.status_code, 200)
        article = Article.objects.first()
        self.assertEqual(article.title, "Updated title")

    def test_delete_post_if_not_exists(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.user.token)
        response = self.client.delete("/blog/articles/1/")
        self.assertEqual(response.status_code, 404)

    def test_delete_post_if_not_authorized(self):
        Article.objects.create(
            title="Article title", text="Article text", author=self.user
        )
        response = self.client.delete("/blog/articles/1/")
        self.assertEqual(response.status_code, 403)

    def test_delete_post_if_not_author(self):
        Article.objects.create(
            title="Article title", text="Article text", author=self.user2
        )
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.user.token)
        response = self.client.delete("/blog/articles/1/")
        self.assertEqual(response.status_code, 403)

    def test_delete_post_successfully(self):
        Article.objects.create(
            title="Article title", text="Article text", author=self.user
        )
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.user.token)
        response = self.client.delete("/blog/articles/1/")
        self.assertEqual(response.status_code, 204)
        article = Article.objects.all()
        self.assertEqual(article.count(), 0)


class TestLikeApiView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="user", email="email@mail.com", password="password"
        )
        cls.article = Article.objects.create(
            title="Article title", text="Article text", author=cls.user
        )

    @unittest.skip
    def test_like_if_not_authorized(self):
        response = self.client.get("/blog/articles/1/like/")
        self.assertEqual(response.status_code, 403)

    @unittest.skip
    def test_like_if_post_not_exists(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.user.token)
        response = self.client.get("/blog/articles/2/like/")
        self.assertEqual(response.status_code, 404)

    @unittest.skip
    def test_like_if_post_not_liked_yet(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.user.token)
        response = self.client.get("/blog/articles/1/like/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["detail"], "Article was liked")

    @unittest.skip
    def test_like_if_post_was_liked(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.user.token)
        self.client.get("/blog/articles/1/like/")
        response = self.client.get("/blog/articles/1/like/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["detail"], "Article was unliked")
