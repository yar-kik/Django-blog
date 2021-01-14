from django.contrib.auth.models import User
from django.test import TestCase

from articles.models import Article, Comment


class TestArticleView(TestCase):
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
        cls.admin = User.objects.create_superuser(
            username='admin',
            email='mail@mail.com',
            password='pass'
        )
        cls.comment = Comment.objects.create(
            name=cls.user,
            body="Test",
            article=cls.article
        )

    def test_publish_list(self):
        response = self.client.get('/articles/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'articles/post/list.html')

    def test_moderation_list_user(self):
        response = self.client.get('/articles/moderation_list/')
        self.assertEqual(response.status_code, 403)

    def test_moderation_list_admin(self):
        self.client.login(username='admin',
                          password='pass')
        response = self.client.get('/articles/moderation_list/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'articles/post/list.html')

    def test_draft_list_user(self):
        response = self.client.get('/articles/draft_list/')
        self.assertEqual(response.status_code, 403)

    def test_draft_list_admin(self):
        self.client.login(username='admin',
                          password='pass')
        response = self.client.get('/articles/draft_list/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'articles/post/list.html')

    def test_film_articles_list(self):
        response = self.client.get('/articles/film_articles/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'articles/post/list.html')
        self.assertEqual(response.context["section"], "film")

    def test_anime_articles_list(self):
        response = self.client.get('/articles/anime_articles/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'articles/post/list.html')
        self.assertEqual(response.context["section"], "anime")

    def test_game_articles_list(self):
        response = self.client.get('/articles/game_articles/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'articles/post/list.html')
        self.assertEqual(response.context["section"], "game")

    def test_article_detail(self):
        response = self.client.get(self.article.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'articles/post/detail.html')
        self.assertEqual(response.context["section"], self.article.category)

    def test_comment_list(self):
        response = self.client.get(f"/articles/{self.article.id}/all_comments/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'articles/comment/partial_comments_all.html')
