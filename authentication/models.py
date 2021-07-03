from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.db import models


class UserManager(BaseUserManager):
    """Custom user manager class"""

    def create_user(
        self, username: str, email: str, password: str = None
    ) -> "User":
        """Create and return user with username, email and password"""
        if username is None:
            raise TypeError("Users must have a username")
        if email is None:
            raise TypeError("Users must have a email")
        user: "User" = self.model(
            username=username, email=self.normalize_email(email)
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username: str, email: str, password: str):
        """Create and return user with admin rights"""
        if password is None:
            raise TypeError("Superusers must have a password")
        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        db_index=True,
        max_length=32,
        unique=True,
        validators=[ASCIIUsernameValidator()],
    )
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    registered = models.DateTimeField(auto_now_add=True)
    last_request = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]
    objects = UserManager()

    def __str__(self) -> str:
        """Return string representation of model"""
        return self.username

    @property
    def token(self) -> str:
        """Return user token"""
        return self._generate_jwt_token()

    def _generate_jwt_token(self) -> str:
        """Generate JWT token with user id and status"""
        payload = {
            "exp": datetime.utcnow() + timedelta(**settings.TOKEN_EXPIRATION),
            "iat": datetime.utcnow(),
            "sub": self.pk,
            "admin": self.is_superuser,
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")