from rest_framework.test import APITestCase

from authentication.models import User


class TestUserModel(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="user", email="email@mail.com", password="password"
        )

    def test_str(self):
        self.assertEqual(str(self.user), "user")

    def test_user_token(self):
        self.assertIsInstance(self.user.token, str)


class TestUserManager(APITestCase):
    def test_create_user_without_username(self):
        with self.assertRaises(TypeError):
            User.objects.create_user(
                email="email@mail.com", password="password"
            )

    def test_create_user_without_email(self):
        with self.assertRaises(TypeError):
            User.objects.create_user(username="user", password="password")

    def test_create_user_successfully(self):
        user = User.objects.create_user(
            username="user", email="email@mail.com", password="password"
        )
        self.assertIsInstance(user, User)
