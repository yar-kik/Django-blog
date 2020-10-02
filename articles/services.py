from django.contrib.auth.models import User

from articles.forms import CommentForm
from articles.models import Comment


def create_reply_form(request, comment_form: CommentForm, parent_comment: Comment) -> CommentForm:
    if comment_form.is_valid():
        new_comment = comment_form.save(commit=False)
        new_comment.article_id = parent_comment.article_id
        new_comment.name = request.user
        new_comment.path.extend(parent_comment.path)
        new_comment.reply_to_id = parent_comment.name_id
        return new_comment


def create_comment_form(request, comment_form: CommentForm, article_id: int) -> Comment:
    if comment_form.is_valid():
        new_comment = comment_form.save(commit=False)
        new_comment.article_id = article_id
        new_comment.name = request.user
        return new_comment


def is_author(request, comment: Comment) -> bool:
    user = request.user
    if user.is_staff or comment.name_id == user.id:
        return True
    else:
        return False
