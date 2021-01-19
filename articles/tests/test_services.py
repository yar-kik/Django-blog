from django.contrib.auth.models import User
from django.test import TestCase, Client, RequestFactory

from articles.forms import CommentForm
from articles.models import Article, Comment
from articles import services


class TestArticleServices(TestCase):
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

    def test_create_reply_form(self):
        comment_form = CommentForm(data={"body": 'some comment'})
        self.client.login(username='user', password='pass')
        request = self.client.get('/article/').wsgi_request
        new_comment = services.create_reply_form(request, comment_form, self.comment)
        new_comment.save()
        self.assertEqual(new_comment.name, self.user)
        self.assertEqual(new_comment.reply_to, self.comment.name)
        self.assertEqual(new_comment.path, [1, 2])

