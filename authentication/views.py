from datetime import datetime

from django.utils import timezone
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import (
    LoginSerializer,
    RegistrationSerializer,
)


class RegistrationApiView(APIView):
    serializer_class = RegistrationSerializer

    def post(self, request: Request) -> Response:
        """Register new user"""
        user = request.data.get("user", {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"user": serializer.data}, status=status.HTTP_201_CREATED
        )


class LoginApiView(APIView):
    serializer_class = LoginSerializer

    def post(self, request: Request) -> Response:
        """Login user"""
        user_data = request.data.get("user", {})
        serializer = self.serializer_class(data=user_data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(username=user_data.get("username"))
        user.last_login = datetime.now(tz=timezone.utc)
        user.save()
        return Response({"user": serializer.data}, status=status.HTTP_200_OK)
