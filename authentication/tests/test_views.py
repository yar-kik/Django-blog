"""Module to test auth app views"""

from rest_framework.test import APITestCase

from authentication.models import User


class TestRegistrationApiView(APITestCase):
    """Test user registration"""

    def test_register_if_invalid_data(self):
        """Testing user register if data is invalid"""
        response = self.client.post(
            "/auth/registration/",
            data={
                "user": {
                    "username": "fake user",
                    "email": "email@mail",
                    "password": "pass",
                }
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_create_post_if_empty_input(self):
        """Testing create post if input is empty"""
        response = self.client.post(
            "/auth/registration/",
            data={
                "user": {
                    "username": "user",
                    "email": "email@mail.com",
                    "password": "password",
                }
            },
        )
        self.assertEqual(response.status_code, 201)


class TestLoginApiView(APITestCase):
    """Test user login"""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="user", email="email@mail.com", password="password"
        )

    def test_login_if_user_not_exists_or_wrong_password(self):
        """Testing login if user not exists or password is wrong"""
        response = self.client.post(
            "/auth/login/",
            data={"user": {"username": "fake_user", "password": "somepass"}},
        )
        self.assertEqual(response.status_code, 400)

    def test_successful_login(self):
        """Testing successful login"""
        response = self.client.post(
            "/auth/login/",
            data={"user": {"username": "user", "password": "password"}},
        )
        self.assertEqual(response.status_code, 200)
