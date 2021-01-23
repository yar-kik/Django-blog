from django.contrib.auth.models import User
from django.test import TestCase

from articles.models import Article, Comment


class TestArticleView(TestCase):

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

    def test_articles_redirect(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 301)

    def test_publish_list(self):
        response = self.client.get('/articles/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'articles/post/list.html')

    def test_moderation_list(self):
        self.client.login(username='admin',
                          password='pass')
        response = self.client.get('/articles/moderation_list/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'articles/post/list.html')

    def test_draft_list(self):
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


class TestCommentView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='user',
            password='pass',
            email='e@mail.com'
        )
        cls.article = Article.objects.create(
            title="First article",
            author=cls.user,
            text='Some text',
            status='publish'
        )
        cls.comment = Comment.objects.create(
            name=cls.user,
            body="Test",
            article=cls.article
        )
        cls.user2 = User.objects.create_user(
            username='user2',
            password='pass',
            email='e2@mail.com'
        )

    def test_comment_list(self):
        response = self.client.get(f"/articles/{self.article.id}/all_comments/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'articles/comment/partial_comments_all.html')

    def test_create_comment(self):
        self.client.login(username='user', password='pass')
        response = self.client.get(
            f"/articles/{self.article.id}/create_comment/",
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            f"/articles/{self.article.id}/create_comment/",
            data={"name": self.user.id,
                  "body": 'New comment'},
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)

    def test_edit_comment_not_author(self):
        self.client.login(username='user2', password='pass')
        response = self.client.post(
            f"/articles/{self.comment.id}/update_comment/",
            data={"body": 'Updated comment'},
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 403)

    def test_edit_comment(self):
        self.client.login(username='user', password='pass')
        response = self.client.get(
            f"/articles/{self.comment.id}/update_comment/",
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            f"/articles/{self.comment.id}/update_comment/",
            data={"body": 'Updated comment'},
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_comment_not_author(self):
        self.client.login(username='user2', password='pass')
        response = self.client.post(
            f"/articles/{self.comment.id}/delete_comment/",
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 403)

    def test_delete_comment(self):
        self.client.login(username='user', password='pass')
        response = self.client.get(
            f"/articles/{self.comment.id}/delete_comment/",
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            f"/articles/{self.comment.id}/delete_comment/",
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)

    def test_article_like(self):
        self.client.login(username='user', password='pass')
        response = self.client.post("/articles/like_article/",
                                    date={"id": 1, "action": 'like'})
        self.assertEqual(response.status_code, 200)

    def test_bookmark_article(self):
        self.client.login(username='user', password='pass')
        response = self.client.post("/articles/bookmark_article/",
                                    date={"id": 1, "action": 'like'})
        self.assertEqual(response.status_code, 200)
