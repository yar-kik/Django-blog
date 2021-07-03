"""Module to test auth models"""

from rest_framework.test import APITestCase

from authentication.models import User


class TestUserModel(APITestCase):
    """Test custom user model"""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="user", email="email@mail.com", password="password"
        )

    def test_str(self):
        """Testing user model string representation"""

        self.assertEqual(str(self.user), "user")

    def test_user_token(self):
        """Testing user token"""

        self.assertIsInstance(self.user.token, str)


class TestUserManager(APITestCase):
    """Test custom user manager"""

    def test_create_user_without_username(self):
        """Testing user creating if username isn't provided"""

        with self.assertRaises(TypeError):
            # pylint: disable=no-value-for-parameter
            User.objects.create_user(
                email="email@mail.com", password="password"
            )

    def test_create_user_without_email(self):
        """Testing user creating if email isn't provided"""

        with self.assertRaises(TypeError):
            # pylint: disable=no-value-for-parameter
            User.objects.create_user(username="user", password="password")

    def test_create_user_successfully(self):
        """Testing successful user creating"""

        user = User.objects.create_user(
            username="user", email="email@mail.com", password="password"
        )
        self.assertIsInstance(user, User)
