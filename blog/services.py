from typing import Union

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import QuerySet
from django.http import HttpRequest, JsonResponse
from django.template.loader import render_to_string

from blog.models import Comment, Article
from blog.selectors import get_comments_by_id


def is_author(request: HttpRequest, comment: Comment) -> bool:
    """
    Check if the user is the author
    """
    user = request.user
    if user.is_authenticated:
        if user.is_staff or comment.name_id == user.id:
            return True
    return False


def paginate_articles(
    request: HttpRequest, object_list: Article, paginate_by: int = 6
) -> QuerySet:
    """
    Get QuerySet of Article model and return paginated blog
    """
    paginator = Paginator(object_list, paginate_by)
    page = request.GET.get("page")
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    return articles


def paginate_comments(
    request: HttpRequest, object_list: Comment, paginate_by: int = 16
) -> Union[QuerySet, None]:
    """
    Get QuerySet of Comment model and return paginated comments
    """
    paginator = Paginator(object_list, paginate_by)
    page = request.GET.get("page")
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        return None
    return comments


def save_comment(request, template, form, **kwargs):
    """
    Функція збереження коментарю (при створенні, зміні чи видаленні) через AJAX.
    Data містить значення про валідність коментарю, його форма (при видаленні чи редагуванні),
    шаблон із усіма коментарями даної статті
    """
    data = dict()
    if request.method == "POST":
        article_id = form.instance.article_id
        comments = get_comments_by_id(article_id)
        if form.is_valid():
            context = {"comments": comments, "user": request.user}
            form.save()
            data["form_is_valid"] = True
            data["html_comments_all"] = render_to_string(
                "blog/comment/partial_comments_all.html", context
            )
        else:
            data["form_is_valid"] = False
    else:
        context = {"form": form, "user": request.user}
        if kwargs:
            context["comment_id"] = kwargs["comment_id"]
            data["action"] = kwargs["action"]
        data["html_form"] = render_to_string(
            template, context, request=request
        )
    return JsonResponse(data)
