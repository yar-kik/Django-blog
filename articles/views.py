import logging
import redis
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from rest_framework.generics import ListCreateAPIView, \
    RetrieveUpdateDestroyAPIView

from common.decorators import ajax_required
from .models import Article, Comment
from .selectors import (
    get_article_by_slug,
    get_parent_comment,
    get_comments_by_id,
    get_moderation_articles,
    get_published_articles,
    get_draft_articles,
    get_film_articles,
    get_anime_articles,
    get_game_articles,
)
from .serializers import ArticleSerializer
from .services import (
    is_author,
    paginate_articles,
    save_comment,
    paginate_comments,
)

logger = logging.getLogger(__name__)

r = redis.StrictRedis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB
)


def publish_list(request):
    """
    Show all published articles
    """
    object_list = get_published_articles()
    articles = paginate_articles(request, object_list)
    return render(request, "articles/post/list.html", {"articles": articles})


@permission_required("articles.can_moderate_article", raise_exception=True)
def moderation_list(request):
    """
    Show articles on moderation
    """
    object_list = get_moderation_articles()
    articles = paginate_articles(request, object_list)
    return render(request, "articles/post/list.html", {"articles": articles})


@permission_required("articles.can_draft_article", raise_exception=True)
def draft_list(request):
    """
    Show all draft articles
    """
    object_list = get_draft_articles(request)
    articles = paginate_articles(request, object_list)
    return render(request, "articles/post/list.html", {"articles": articles})


def film_articles_list(request):
    """
    Show articles in category films
    """
    object_list = get_film_articles()
    articles = paginate_articles(request, object_list)
    return render(
        request,
        "articles/post/list.html",
        {"section": "film", "articles": articles},
    )


def anime_articles_list(request):
    """
    Show articles in category anime
    """
    object_list = get_anime_articles()
    articles = paginate_articles(request, object_list)
    return render(
        request,
        "articles/post/list.html",
        {"section": "anime", "articles": articles},
    )


def game_articles_list(request):
    """
    Show articles in category games
    """
    object_list = get_game_articles()
    articles = paginate_articles(request, object_list)
    return render(
        request,
        "articles/post/list.html",
        {"section": "game", "articles": articles},
    )


def article_detail(request, slug):
    """
    Show details of the article
    """
    article = get_article_by_slug(slug=slug, annotate=True)
    comment_form = CommentForm()
    total_views = r.incr(f"article:{article.id}:views")
    return render(
        request,
        "articles/post/detail.html",
        {
            "article": article,
            "section": article.category,
            "comment_form": comment_form,
            "total_views": total_views,
        },
    )


def comments_list(request, article_id):
    """
    Show all paginated comments of the article
    """
    comments = get_comments_by_id(article_id)
    paginated_comments = paginate_comments(request, comments)
    if paginated_comments is None:
        return HttpResponse("")
    return render(
        request,
        "articles/comment/partial_comments_all.html",
        {"comments": paginated_comments},
    )


@ajax_required
@login_required
def reply_comment(request, comment_id):
    """
    Create reply of the parent comment
    """
    parent_comment = get_parent_comment(comment_id)
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        create_reply_form(request, comment_form, parent_comment)
    else:
        comment_form = CommentForm()
    return save_comment(
        request,
        "articles/comment/partial_comment_create.html",
        comment_form,
        action="reply",
        comment_id=comment_id,
    )


@ajax_required
@login_required
def create_comment(request, article_id):
    """
    Create an article comment
    """
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        create_comment_form(request, comment_form, article_id)
    else:
        comment_form = CommentForm()
    return save_comment(
        request, "articles/comment/partial_comments_all.html", comment_form
    )


@ajax_required
def edit_comment(request, comment_id):
    """
    Edit an article comment
    """
    instance_comment = get_object_or_404(Comment, id=comment_id)
    if not is_author(request, instance_comment):
        return HttpResponseForbidden()
    if request.method == "POST":
        comment_form = CommentForm(
            instance=instance_comment, data=request.POST
        )
    else:
        comment_form = CommentForm(instance=instance_comment)
    return save_comment(
        request, "articles/comment/partial_comment_edit.html", comment_form
    )


@ajax_required
def delete_comment(request, comment_id):
    """
    delete an article comment
    """
    comment = get_object_or_404(Comment, id=comment_id)
    if not is_author(request, comment):
        return HttpResponseForbidden()
    article_id = comment.article_id
    comments = get_comments_by_id(article_id)
    data = dict()
    if request.method == "POST":
        comment.delete()
        data["form_is_valid"] = True
        data["html_comments_all"] = render_to_string(
            "articles/comment/partial_comments_all.html",
            {"comments": comments, "user": request.user},
        )
    else:
        data["html_form"] = render_to_string(
            "articles/comment/partial_comment_delete.html",
            {"comment": comment, "user": request.user},
            request=request,
        )
    return JsonResponse(data)


class ListArticleApiView(ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class SingleArticleApiView(RetrieveUpdateDestroyAPIView):
    lookup_field = 'slug'
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


@require_POST
@login_required
def article_like(request):
    """
    Function to like the article
    """
    article_id = request.POST.get("id")
    action = request.POST.get("action")
    if article_id and action:
        article = get_object_or_404(Article, id=article_id)
        if action == "like":
            article.users_like.add(request.user)
        else:
            article.users_like.remove(request.user)
        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "404"})


def article_search(request):
    """Пошук статті і використанням вектору пошуку (за полями заголовку і тексту з
    ваговими коефіцієнтами 1 та 0.4 відповідно. Пошуковий набір проходить стемінг.
    При пошуку враховується близькість шуканих слів одне до одного"""
    query = ""
    results = []
    if "query" in request.GET:
        results, query = search_results(request)
    return render(
        request,
        "articles/post/search.html",
        {"query": query, "results": results},
    )


@login_required
@require_POST
def bookmark_article(request):
    """
    Add or remove article from bookmarked articles of user
    """
    article_id = request.POST.get("id")
    action = request.POST.get("action")
    if article_id and action:
        article = get_object_or_404(Article, id=article_id)
        if action == "bookmark":
            article.users_bookmark.add(request.user)
        else:
            article.users_bookmark.remove(request.user)
        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "404"})
