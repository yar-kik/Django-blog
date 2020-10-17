from typing import Union

from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import QuerySet
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.template.loader import render_to_string

from articles.forms import CommentForm, SearchForm
from articles.models import Comment, Article
from articles.selectors import get_comments_by_id


def create_reply_form(request: HttpRequest, comment_form: CommentForm, parent_comment: Comment) -> CommentForm:
    """Create reply form using a parent comment"""
    if comment_form.is_valid():
        new_comment = comment_form.save(commit=False)
        new_comment.article_id = parent_comment.article_id
        new_comment.name = request.user
        new_comment.path.extend(parent_comment.path)
        new_comment.reply_to_id = parent_comment.name_id
        return new_comment


def create_comment_form(request: HttpRequest, comment_form: CommentForm, article_id: int) -> Comment:
    """Create comment form using a article's id"""
    if comment_form.is_valid():
        new_comment = comment_form.save(commit=False)
        new_comment.article_id = article_id
        new_comment.name = request.user
        return new_comment


def is_author(request: HttpRequest, comment: Comment) -> bool:
    """Check if the user is the author"""
    user = request.user
    if user.is_staff or comment.name_id == user.id:
        return True
    else:
        return False


def paginate_articles(request: HttpRequest, object_list: Article, paginate_by: int = 3) -> QuerySet:
    """Get QuerySet of Article model and return paginated articles"""
    paginator = Paginator(object_list, paginate_by)
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    return articles


def paginate_comments(request: HttpRequest, object_list: Comment, paginate_by: int = 16) -> Union[QuerySet, None]:
    """Get QuerySet of Comment model and return paginated comments"""
    paginator = Paginator(object_list, paginate_by)
    page = request.GET.get('page')
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        return None
    return comments


def save_comment(request, template, form, **kwargs):
    """Функція збереження коментарю (при створенні, зміні чи видаленні) через AJAX.
    Data містить значення про валідність коментарю, його форма (при видаленні чи редагуванні),
    шаблон із усіма коментарями даної статті"""
    data = dict()
    if request.method == 'POST':
        article_id = form.instance.article_id
        comments = get_comments_by_id(article_id)
        if form.is_valid():
            context = {'comments': comments, 'user': request.user}
            form.save()
            data['form_is_valid'] = True
            data['html_comments_all'] = render_to_string('articles/comment/partial_comments_all.html',
                                                         context)
        else:
            data['form_is_valid'] = False
    else:
        context = {'form': form, 'user': request.user}
        if kwargs:
            context['comment_id'] = kwargs['comment_id']
            data['action'] = kwargs['action']
        data['html_form'] = render_to_string(template, context, request=request)
    return JsonResponse(data)


def search_results(request):
    """Пошук статті і використанням вектору пошуку (за полями заголовку і тексту з
    ваговими коефіцієнтами 1 та 0.4 відповідно. Пошуковий набір проходить стемінг.
    При пошуку враховується близькість шуканих слів одне до одного"""
    form = SearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data['query']
        search_vector = SearchVector('title', weight='A', config='russian') + SearchVector('text', weight='B',
                                                                                           config='russian')
        search_query = SearchQuery(query, config='russian')
        results = Article.objects.annotate(search=search_vector, rank=SearchRank(search_vector, search_query)).\
            filter(rank__gte=0.3).order_by('-rank')
        return results, query


def search_results2(request):
    """Search using trigram similarity"""
    form = SearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data['query']
        results = Article.objects.annotate(
            similarity=TrigramSimilarity('title', query),
        ).filter(similarity__gt=0.2).order_by('-similarity')
        return results, query
