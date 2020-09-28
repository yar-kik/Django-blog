from articles.forms import CommentForm
from articles.models import Comment


def create_reply_form(request, comment_form: CommentForm, parent_comment: Comment) -> CommentForm:
    if comment_form.is_valid():
        new_comment = comment_form.save(commit=False)
        new_comment.article = parent_comment.article
        new_comment.name = request.user
        new_comment.path.extend(parent_comment.path)
        new_comment.reply_to = parent_comment.name
        return new_comment


def create_comment_form(request, comment_form: CommentForm, article_id: int) -> Comment:
    if comment_form.is_valid():
        new_comment = comment_form.save(commit=False)
        new_comment.article_id = article_id
        new_comment.name = request.user
        return new_comment


