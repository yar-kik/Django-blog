from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
import redis
from django.conf import settings
from actions.utils import create_action
from common.decorators import ajax_required
from .forms import ImageCreateForm
from .models import Image

# Підключення до Redis
r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)


@login_required
def image_create(request):
    """"""
    if request.method == "POST":
        """Форма відправлена"""
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            """Данні форми коректні"""
            cd = form.cleaned_data
            new_item = form.save(commit=False)
            """Додаємо користувача до створеного об'єкту"""
            new_item.user = request.user
            new_item.save()
            create_action(request.user, 'bookmarked image', new_item)
            messages.success(request, 'Image added successfully')
            """Перенаправляємо користувача на сторінку збереженого зображення"""
            return redirect(new_item.get_absolute_url())
    else:
        """Заповнюємо форму із GET-запиту"""
        form = ImageCreateForm(data=request.GET)
    return render(request, 'images/image/create.html',
                  {'section': 'images', 'form': form})


def image_detail(request, id, slug):
    """"""
    image = get_object_or_404(Image, id=id, slug=slug)
    # Збільшуємо кількість переглядів зображення на 1
    total_views = r.incr(f'image:{image.id}:views')
    r.zincrby('image_ranking', image.id, 1)
    return render(request, 'images/image/detail.html',
                  {'section': 'images', 'image': image, 'total_views': total_views})


@login_required
@require_POST  # Виконання тільки методу POST
def image_like(request):
    """ID зображення, для якого виконується дія"""
    image_id = request.POST.get('id')
    """Дія, яку хоче виконати користувач 'like' чи 'unlike'"""
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
                create_action(request.user, 'likes', image)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'ok'})


# @ajax_required
@login_required
# @require_POST
def image_list(request):
    """"""
    images = Image.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # Если переданная страница не является числом, возвращаем первую.
        images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            # Если получили AJAX-запрос с номером страницы, большим, чем их количество,
            # возвращаем пустую страницу.
            return HttpResponse('')
        # Если номер страницы больше, чем их количество, возвращаем последнюю.
        images = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request, 'images/image/list_ajax.html',
                      {'section': 'images', 'images': images})
    return render(request, 'images/image/list.html',
                  {'section': 'images', 'images': images})


@login_required
def image_ranking(request):
    """"""
    # # Отримуємо набір рейтингу картинок (з відсортованого масиву з першого по останній елемент)
    image_ranking = r.zrange('image_ranking', 0, -1, desc=True)[:10]
    # image_ranking_ids = [int(id) for id in image_ranking]
    # # Отримуємо відсорторований список найпопулярніших картинок
    # most_viewed = list(Image.objects.filter(id__in=image_ranking_ids))
    # most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))
    most_viewed = list(Image.objects.all())
    return render(request, 'images/image/ranking.html', {'section': 'images',
                                                         'most_viewed': most_viewed,
                                                         'im_r': image_ranking})
