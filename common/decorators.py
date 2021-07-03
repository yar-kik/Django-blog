from django.core.exceptions import PermissionDenied
from functools import wraps

from django.http import HttpRequest
from django.shortcuts import get_object_or_404

from blog.models import Comment


def ajax_required(view):
    """
    Decorator for views that checks that the request is ajax, raising
    PermissionDenied if necessary.
    """

    @wraps(view)
    def _wrapped_view(request, *args, **kwargs):
        if not request.is_ajax():
            raise PermissionDenied()
        return view(request, *args, **kwargs)

    return _wrapped_view


def author_or_staff_required(view):
    """
    Decorator that check that the user is the author,
    raising PermissionDenied if necessary
    """

    @wraps(view)
    def _wrapped_view(request: HttpRequest, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        user = request.user
        if user.is_authenticated:
            if user.is_staff or comment.name_id == user.id:
                return view(request, comment_id)
        raise PermissionDenied()

    return _wrapped_view
