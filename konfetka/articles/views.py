from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from taggit.models import Tag
from django.db.models import Count
from uuslug import slugify

from .forms import EmailPostForm, CommentForm
from .models import Article, Comment


def articles_redirect(request):
    return redirect('articles:all_articles', permanent=True)


def all_articles(request, tag_slug=None):
    articles = Article.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        articles = articles.filter(tags__in=[tag])

    paginator = Paginator(articles, 3)
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    return render(request, 'articles/post/list.html', {'page': page,
                                                       'articles': articles,
                                                       'tag': tag,
                                                       'section': 'articles'})


def article_detail(request, year, month, day, slug):
    article = get_object_or_404(Article, slug=slug, date_created__year=year,
                                date_created__month=month, date_created__day=day)
    """Список активних коментарів цієї статті"""
    comments = article.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        """Користувач відправив коментар"""
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            """Створюємо коментар, але не зберегігаємо в базі данних"""
            new_comment = comment_form.save(commit=False)
            """Прив'язуємо коментар до поточної статті"""
            new_comment.article = article
            """Зберігаємо коментар в базі даних"""
            new_comment.save()
    else:
        comment_form = CommentForm()
    """Формуванння списку схожих статей"""

    """Отримання списку id тегів даної статті"""
    article_tags_ids = article.tags.values_list('id', flat=True)
    """Всі статті, що містять хоча б один заданий тег (за виключенням поточної статті)"""
    similar_articles = Article.objects.filter(tags__in=article_tags_ids).exclude(id=article.id)
    """Сортування статей в порядку зменшення кількості схожих тегів та дати."""
    similar_articles = similar_articles.annotate(same_tags=Count('tags')).order_by('-same_tags', '-date_created')[:4]
    return render(request, 'articles/post/detail.html', {'article': article,
                                                         'comments': comments,
                                                         'new_comment': new_comment,
                                                         'comment_form': comment_form,
                                                         'similar_articles': similar_articles,
                                                         'section': 'articles'})


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


class CreateArticle(LoginRequiredMixin, CreateView):
    """Функція публікації статті"""
    model = Article
    fields = ['title', 'text', 'tags']
    template_name = 'articles/post/create_article.html'

    # success_url = 'articles:all_articles'
    # def form_valid(self, form):
    #     self.object = form.save(commit=False)
    #     self.object.author = self.request.user
    #     self.object.slug = slugify(self.object.title)
    #     self.object.save()
    #     return super().form_valid(form)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)


class UpdateArticle(LoginRequiredMixin, UpdateView):
    """"""
    model = Article
    fields = ['title', 'text', 'tags']
    template_name = 'articles/post/update_article.html'
    # success_url = reverse_lazy('articles:update_article')


class DeleteArticle(LoginRequiredMixin, DeleteView):
    """"""
    model = Article
    template_name = 'articles/post/delete_article.html'
    success_url = reverse_lazy('articles:all_articles')
