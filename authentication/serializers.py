from datetime import datetime

from django.contrib.auth import authenticate
from django.utils import timezone

from rest_framework import serializers

from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration and creation a new one"""

    password = serializers.CharField(
        max_length=64, min_length=8, write_only=True
    )

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        """Create new user with validated data"""
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    """Class for user logging data deserialization"""

    username = serializers.CharField(max_length=32)
    password = serializers.CharField(max_length=64, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError(
                "User doesn't exist or wrong password"
            )
        if not user.is_active:
            raise serializers.ValidationError("This user has been deactivated")
        user.last_login = datetime.now(tz=timezone.utc)
        user.save()
        return {"username": user.username, "token": user.token}


class UserActivitySerializer(serializers.ModelSerializer):
    """Serializer for user activity"""

    class Meta:
        model = User
        fields = ("username", "registered", "last_login", "last_request")
        read_only_fields = (
            "username",
            "registered",
            "last_login",
            "last_request",
        )
