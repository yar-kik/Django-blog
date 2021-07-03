"""Auth middlewares module"""

from datetime import datetime

from django.utils import timezone
from rest_framework.request import Request
from rest_framework.response import Response


class UserActivityMiddleware:
    """Save last user request"""

    def __init__(self, get_response: Response):
        self.get_response = get_response

    def __call__(self, request: Request) -> Response:
        response = self.get_response(request)
        user = request.user
        if user.is_authenticated:
            user.last_request = datetime.now(tz=timezone.utc)
            user.save()
        return response
