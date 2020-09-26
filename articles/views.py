import redis
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.db.models import Count
from uuslug import slugify

# from actions.utils import create_action
from .forms import EmailPostForm, CommentForm, ArticleForm, SearchForm
from .models import Article, Comment
from .selectors import get_article, get_comments, get_parent_comment
from .services import create_comment_form, create_reply_form
from .tagging import CustomTag

r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)


def articles_redirect(request):
    return redirect('articles:all_articles', permanent=True)


class ArticlesList(ListView):
    """Клас списку коментарів із пагінацією"""
    model = Article
    template_name = 'articles/post/list.html'
    context_object_name = 'articles'
    extra_context = {'section': 'articles'}
    paginate_by = 3

    def paginate_queryset(self, queryset, page_size):
        """Функція пагінації набору даних з обробкою виключень GET-запитів"""
        paginator = self.get_paginator(queryset, page_size)
        page_kwargs = self.page_kwarg
        page = self.kwargs.get(page_kwargs) or self.request.GET.get('page')
        try:
            page = paginator.page(page)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)
        finally:
            return paginator, page, page.object_list, page.has_other_pages()

    def get_queryset(self):
        """Отримання набору даних з можливістю відсортувати дані за тегами"""
        queryset = super().get_queryset().select_related('author').\
            annotate(total_comments=Count('comments'),
                     total_likes=Count('users_like'))
        if self.kwargs:
            return queryset.filter(tags__slug__in=[self.kwargs['tag_slug']])
        else:
            return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        """Введення в контекст шаблону тегів"""
        context = super().get_context_data(**kwargs)
        if self.kwargs:
            context['tag'] = get_object_or_404(CustomTag, slug=self.kwargs['tag_slug'])
        return context


# @cache_page(60 * 15)
def article_detail(request, slug):
    article = get_article(slug=slug)
    comments = get_comments(article)
    comment_form = CommentForm()
    total_views = r.incr(f'article:{article.id}:views')

    """Формуванння списку схожих статей"""

    """Отримання списку id тегів даної статті"""
    # article_tags_ids = article.tags.values_list('id', flat=True)
    """Всі статті, що містять хоча б один заданий тег (за виключенням поточної статті)"""
    # similar_articles = Article.objects.filter(tags__in=article_tags_ids).exclude(id=article.id)
    """Сортування статей в порядку зменшення кількості схожих тегів та дати."""
    # similar_articles = similar_articles.annotate(same_tags=Count('tags')).order_by('-same_tags', '-date_created')[:4]
    return render(request, 'articles/post/detail.html', {'article': article,
                                                         # 'similar_articles': similar_articles,
                                                         'comments': comments,
                                                         'section': 'articles',
                                                         'comment_form': comment_form,
                                                         'total_views': total_views})


# @login_required
# def comments_list(request):
#     """"""
#     comments = get_comments()
#     paginator = Paginator(comments, 8)
#     page = request.GET.get('page')
#     try:
#         images = paginator.page(page)
#     except PageNotAnInteger:
#         # Если переданная страница не является числом, возвращаем первую.
#         images = paginator.page(1)
#     except EmptyPage:
#         if request.is_ajax():
#             # Если получили AJAX-запрос с номером страницы, большим, чем их количество,
#             # возвращаем пустую страницу.
#             return HttpResponse('')
#         # Если номер страницы больше, чем их количество, возвращаем последнюю.
#         images = paginator.page(paginator.num_pages)
#     if request.is_ajax():
#         return render(request, 'images/image/list_ajax.html',
#                       {'section': 'images', 'images': images})
#     return render(request, 'images/image/list.html',
#                   {'section': 'images', 'images': images})


def save_comment(request, template, form, **kwargs):
    """Функція збереження коментарю (при створенні, зміні чи видаленні) через AJAX.
    Data містить значення про валідність коментарю, його форма (при видаленні чи редагуванні),
    шаблон із усіма коментарями даної статті"""
    data = dict()
    if request.method == 'POST':
        article = form.instance.article
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            comments = get_comments(article)
            data['html_comments_all'] = render_to_string('articles/comment/partial_comments_all.html',
                                                         {'comments': comments})
        else:
            data['form_is_valid'] = False
    else:
        context = {'form': form}
        data['html_form'] = render_to_string(template, context, request=request)
        if kwargs:
            context['comment_id'] = kwargs['comment_id']
            data['action'] = kwargs['action']
    return JsonResponse(data)


def reply_comment(request, comment_id):
    parent_comment = get_parent_comment(comment_id)
    data = dict()
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        create_reply_form(request, comment_form, parent_comment)
        return save_comment(request, 'articles/comment/partial_comments_all.html', comment_form)
    else:
        comment_form = CommentForm()
        context = {'form': comment_form, 'comment_id': comment_id}
        data['action'] = 'reply'
        data['html_form'] = render_to_string('articles/comment/partial_comment_create.html', context, request=request)
        return JsonResponse(data)


def create_comment(request, article_id):
    """Створення коментарю із закріпленням до статті та користувача-автора"""
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        create_comment_form(request, comment_form, article_id)
    else:
        comment_form = CommentForm()
    return save_comment(request, 'articles/comment/partial_comments_all.html', comment_form)


def edit_comment(request, comment_id):
    """Редагування коментарю, значення якого отримується через id"""
    instance_comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        comment_form = CommentForm(instance=instance_comment, data=request.POST)
    else:
        comment_form = CommentForm(instance=instance_comment)
    return save_comment(request, 'articles/comment/partial_comment_edit.html', comment_form)


def delete_comment(request, comment_id):
    """Видалення коментарю, отриманого через його id."""
    comment = get_object_or_404(Comment, id=comment_id)
    article = comment.article
    comments = get_comments(article)
    data = dict()
    if request.method == 'POST':
        comment.delete()
        data['form_is_valid'] = True
        data['html_comments_all'] = render_to_string('articles/comment/partial_comments_all.html', {
            'comments': comments
        })
    else:
        context = {'comment': comment}
        data['html_form'] = render_to_string('articles/comment/partial_comment_delete.html', context, request=request)
    return JsonResponse(data)


def post_share(request, article_id):
    """Отримання статті по ідентифікатору"""
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


class CreateArticle(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    """Клас створення статті (необхідний відповідний дозвіл)"""
    form_class = ArticleForm
    template_name = 'articles/post/create_article.html'
    permission_required = 'articles.add_article'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)


class UpdateArticle(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    """Класс редагування статті (необхідний дозвіл на це)"""
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


def article_search(request):
    """Пошук статті і використанням вектору пошуку (за полями заголовку і тексту з
    ваговими коефіцієнтами 1 та 0.4 відповідно. Пошуковий набір проходить стемінг.
    При пошуку враховується близькість шуканих слів одне до одного"""
    form = SearchForm()
    query = ''
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', weight='A', config='russian') + SearchVector('text', weight='B',
                                                                                               config='russian')
            search_query = SearchQuery(query, config='russian')
            results = Article.objects.annotate(
                search=search_vector, rank=SearchRank(search_vector, search_query)
            ).filter(rank__gte=0.3).order_by('-rank')
    return render(request, 'articles/post/search.html', {'form': form,
                                                         'query': query,
                                                         'results': results})


def bookmark_article(request):
    article_id = request.POST.get('id')
    action = request.POST.get('action')
    if article_id and action:
        article = Article.objects.only('id', 'users_bookmark').get(id=article_id)
        if action == 'bookmark':
            article.users_bookmark.add(request.user)
        else:
            article.users_bookmark.remove(request.user)
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'ok'})