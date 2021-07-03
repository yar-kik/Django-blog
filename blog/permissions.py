"""Module for custom permissions"""

from rest_framework import permissions
from rest_framework.request import Request


class IsAuthor(permissions.BasePermission):
    """Object permission check if user is author."""

    def has_object_permission(self, request: Request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
