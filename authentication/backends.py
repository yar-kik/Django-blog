"""Module for user authentication"""

from typing import Tuple

import jwt
from django.conf import settings
from rest_framework import authentication, exceptions
from rest_framework.request import Request

from .models import User


class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = "Bearer"

    def authenticate(self, request: Request):
        request.user = None
        auth_header = (
            authentication.get_authorization_header(request)
                .decode("utf-8")
                .split()
        )
        if not auth_header or len(auth_header) == 1 or len(auth_header) > 2:
            return None
        prefix, token = auth_header
        if prefix != self.authentication_header_prefix:
            return None
        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(
            self, request: Request, token: str
    ) -> Tuple[User, str]:
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms="HS256"
            )
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed(
                "Signature expired. Please log in again"
            )
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed(
                "Invalid token. Please log in again."
            )
        try:
            user = User.objects.get(pk=payload["sub"])
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed("User doesn't exist.")
        if not user.is_active:
            raise exceptions.AuthenticationFailed("User is deactivated.")
        return user, token
