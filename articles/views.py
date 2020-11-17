import logging
import redis
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.edit import ModelFormMixin
from uuslug import slugify

# from actions.utils import create_action
from common.decorators import ajax_required, author_or_staff_required
from .forms import EmailPostForm, CommentForm, ArticleForm
from .models import Article, Comment
from .selectors import get_article_by_slug, get_parent_comment, get_comments_by_id, \
    get_moderation_articles, get_published_articles, get_draft_articles, get_film_articles, get_anime_articles, \
    get_game_articles
from .services import create_comment_form, create_reply_form, is_author, paginate_articles, save_comment, \
    paginate_comments, search_results
from .tagging import CustomTag

logger = logging.getLogger(__name__)

r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)


def articles_redirect(request):
    """Redirect to main page"""
    return redirect('articles:all_articles', permanent=True)


def publish_list(request):
    """Show all published articles"""
    object_list = get_published_articles()
    articles = paginate_articles(request, object_list)
    return render(request, 'articles/post/list.html', {'section': 'articles',
                                                       'articles': articles})


@permission_required('articles.can_moderate_article', raise_exception=True)
def moderation_list(request):
    """Show articles on moderation"""
    object_list = get_moderation_articles()
    articles = paginate_articles(request, object_list)
    return render(request, 'articles/post/list.html', {'section': 'articles',
                                                       'articles': articles})


@permission_required('articles.can_draft_article', raise_exception=True)
def draft_list(request):
    """Show draft articles"""
    object_list = get_draft_articles(request)
    articles = paginate_articles(request, object_list)
    return render(request, 'articles/post/list.html', {'section': 'articles',
                                                       'articles': articles})


def film_articles_list(request):
    object_list = get_film_articles()
    articles = paginate_articles(request, object_list)
    return render(request, 'articles/post/list.html', {'section': 'film',
                                                       'articles': articles})


def anime_articles_list(request):
    object_list = get_anime_articles()
    articles = paginate_articles(request, object_list)
    return render(request, 'articles/post/list.html', {'section': 'anime',
                                                       'articles': articles})


def game_articles_list(request):
    object_list = get_game_articles()
    articles = paginate_articles(request, object_list)
    return render(request, 'articles/post/list.html', {'section': 'game',
                                                       'articles': articles})


# @cache_page(60 * 15)
def article_detail(request, slug):
    """Show details of the article"""
    article = get_article_by_slug(slug=slug, annotate=True)
    comment_form = CommentForm()
    total_views = r.incr(f'article:{article.id}:views')
    return render(request, 'articles/post/detail.html', {'article': article,
                                                         'section': article.category,
                                                         'comment_form': comment_form,
                                                         'total_views': total_views})


def comments_list(request, article_id):
    """Show all paginated comments of the article"""
    comments = get_comments_by_id(article_id)
    paginated_comments = paginate_comments(request, comments)
    if paginated_comments is None:
        return HttpResponse('')
    return render(request, 'articles/comment/partial_comments_all.html', {'comments': paginated_comments})


@ajax_required
def reply_comment(request, comment_id):
    """Create reply of the parent comment"""
    parent_comment = get_parent_comment(comment_id)
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        create_reply_form(request, comment_form, parent_comment)
    else:
        comment_form = CommentForm()
    return save_comment(request, 'articles/comment/partial_comment_create.html', comment_form, action='reply',
                        comment_id=comment_id)


@ajax_required
def create_comment(request, article_id):
    """Створення коментарю із закріпленням до статті та користувача-автора"""
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        create_comment_form(request, comment_form, article_id)
    else:
        comment_form = CommentForm()
    return save_comment(request, 'articles/comment/partial_comments_all.html', comment_form)


@ajax_required
def edit_comment(request, comment_id):
    """Редагування коментарю, значення якого отримується через id"""
    instance_comment = get_object_or_404(Comment, id=comment_id)
    if not is_author(request, instance_comment):
        return HttpResponseForbidden
    if request.method == 'POST':
        comment_form = CommentForm(instance=instance_comment, data=request.POST)
    else:
        comment_form = CommentForm(instance=instance_comment)
    return save_comment(request, 'articles/comment/partial_comment_edit.html', comment_form)


# @author_or_staff_required
@ajax_required
def delete_comment(request, comment_id):
    """
    Видалення коментарю, отриманого через його id.
    """
    comment = get_object_or_404(Comment, id=comment_id)
    if not is_author(request, comment):
        return HttpResponseForbidden
    article_id = comment.article_id
    comments = get_comments_by_id(article_id)
    data = dict()
    if request.method == 'POST':
        comment.delete()
        data['form_is_valid'] = True
        data['html_comments_all'] = render_to_string('articles/comment/partial_comments_all.html', {
            'comments': comments, 'user': request.user})
    else:
        data['html_form'] = render_to_string('articles/comment/partial_comment_delete.html',
                                             {'comment': comment, 'user': request.user}, request=request)
    return JsonResponse(data)


def post_share(request, article_id):
    """
    """
    article = get_object_or_404(Article, id=article_id)
    sent = False
    if request.method == 'POST':
        """Форма була відправлена на збереження"""
        form = EmailPostForm(request.POST)
        if form.is_valid():
            """Всі поля форми пройшли валідацію"""
            cd = form.cleaned_data
            article_url = request.build_absolute_uri(article.get_absolute_url())
            subject = f'{cd["name"]} ({cd["email"]}) recommends you reading {article.title}'
            message = f'Read {article.title} at {article_url}\n\n{cd["name"]}\'s comments:' \
                      f'{cd["comments"]}'
            send_mail(subject, message, "einstein16.04@gmail.com", [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'articles/post/share.html', {'article': article,
                                                        'form': form,
                                                        'sent': sent,
                                                        'section': 'articles'})


class ArticleBaseValidation(ModelFormMixin):
    """Base class of article's validation"""
    def form_valid(self, form):
        """Check article's status in a form and assign it"""
        form.instance.author = self.request.user
        form.instance.slug = slugify(form.instance.title)
        if 'draft' in self.request.POST:
            form.instance.status = 'draft'
        elif 'moderation' in self.request.POST:
            form.instance.status = 'moderation'
        elif 'publish' in self.request.POST:
            form.instance.status = 'publish'
        return super().form_valid(form)


class CreateArticle(PermissionRequiredMixin, LoginRequiredMixin, CreateView, ArticleBaseValidation):
    """Клас створення статті (необхідний відповідний дозвіл)"""
    form_class = ArticleForm
    model = Article
    template_name = 'articles/post/create_article.html'
    permission_required = 'articles.add_article'


class UpdateArticle(PermissionRequiredMixin, LoginRequiredMixin, UpdateView, ArticleBaseValidation):
    """Клас редагування статті (необхідний дозвіл на це)"""
    model = Article
    form_class = ArticleForm
    template_name = 'articles/post/update_article.html'
    permission_required = 'articles.change_article'


class DeleteArticle(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    """Видалення статті (необхідний дозвіл або статус персонала)"""
    model = Article
    template_name = 'articles/post/delete_article.html'
    success_url = reverse_lazy('articles:all_articles')
    permission_required = 'articles.delete_article'


@login_required
@require_POST
def article_like(request):
    """Функція уподобання статті"""
    article_id = request.POST.get('id')
    action = request.POST.get('action')
    if article_id and action:
        try:
            article = get_object_or_404(Article, id=article_id)
            if action == 'like':
                article.users_like.add(request.user)
                # create_action(request.user, 'likes', article)
            else:
                article.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'ok'})


# def liked_content(request, content: Article or Comment):
#     """Функція уподобання статті"""
#     content_id = request.POST.get('id')
#     action = request.POST.get('action')
#     if content_id and action:
#         try:
#             content_object = get_object_or_404(content, id=content_id)
#             if action == 'like':
#                 content_object.users_like.add(request.user)
#                 # create_action(request.user, 'likes', article)
#             else:
#                 content_object.users_like.remove(request.user)
#             return JsonResponse({'status': 'ok'})
#         except:
#             pass
#     return JsonResponse({'status': 'ok'})
#
#
# def comment_like(request):
#     """"""
#     liked_content(request, Comment)


def article_search(request):
    """Пошук статті і використанням вектору пошуку (за полями заголовку і тексту з
    ваговими коефіцієнтами 1 та 0.4 відповідно. Пошуковий набір проходить стемінг.
    При пошуку враховується близькість шуканих слів одне до одного"""
    query = ''
    results = []
    if 'query' in request.GET:
        results, query = search_results(request)
    return render(request, 'articles/post/search.html', {'query': query,
                                                         'results': results})


@login_required
@require_POST
def bookmark_article(request):
    """Add or remove article from bookmarked articles"""
    article_id = request.POST.get('id')
    action = request.POST.get('action')
    if article_id and action:
        article = get_object_or_404(Article, id=article_id)
        if action == 'bookmark':
            article.users_bookmark.add(request.user)
        else:
            article.users_bookmark.remove(request.user)
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'ok'})