from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils.http import urlunquote, is_safe_url

from actions.models import Action
from actions.utils import create_action
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm, FeedbackEmailForm
from .models import Profile, Contact
from common.decorators import ajax_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST


def user_login(request):
    """"""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        """Форма заповнена правильно"""
        if form.is_valid():
            """Приводить дані до стандартного вигляду"""
            cd = form.cleaned_data
            """Перевіряються дані на наявність у базі"""
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
        """Користувач є у базі"""
        if user is not None:
            if user.is_active:
                """Запам'ятовується користувач у поточній сесії"""
                login(request, user)
                return HttpResponse('Authenticated successfully')
            else:
                return HttpResponse('Disabled account')
        else:
            return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/registration/login.html', {'form': form})


@login_required
def dashboard(request):
    """За замовчуванням відображаємо всі дії"""
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id', flat=True)
    profile = request.user.profile
    if following_ids:
        """Якщо поточний користувач підписався на когось
        відображаємо тільки дії циї користувачів"""
        actions = actions.filter(user_id__in=following_ids)
    actions = actions.select_related('user', 'user__profile').prefetch_related('target')[:10]

    return render(request, 'account/dashboard.html', {'section': 'dashboard',
                                                      'actions': actions,
                                                      'profile': profile})


def register(request):
    """"""
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        if request.method == 'POST':
            user_form = UserRegistrationForm(request.POST)
            if user_form.is_valid():
                # Створюємо нову форму, але не зберігаємо у базу
                new_user = user_form.save(commit=False)
                # Задаємо користувачу зашифрований пароль
                new_user.set_password(user_form.cleaned_data['password'])
                # Зберігаємо користувача в базі даних
                new_user.save()
                # Створення профілю користувача
                Profile.objects.create(user=new_user)
                new_user = authenticate(request, username=user_form.cleaned_data['username'],
                                        password=user_form.cleaned_data['password'])
                login(request, new_user)
                return redirect('articles:all_articles')
                # create_action(new_user, 'has created an account')
                # return render(request, 'account/register_done.html',
                #               {'new_user': new_user})
        else:
            user_form = UserRegistrationForm()
        return render(request, 'account/register.html',
                      {'user_form': user_form})


@login_required
def edit(request):
    """"""
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {'user_form': user_form,
                                                 'profile_form': profile_form})


@login_required
def user_list(request):
    """Отримує список всіх активних користувачів"""
    users = User.objects.filter(is_active=True)
    return render(request, 'account/user/list.html',
                  {'section': 'people', 'users': users})


@login_required
def user_detail(request, username):
    """За логіном отримує активного користувача (або повертає 404)"""
    user = get_object_or_404(User, username=username, is_active=True)
    return render(request, 'account/user/detail.html',
                  {'section': 'people', 'user': user})


@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user, user_to=user)
                create_action(request.user, 'is following', user)
            else:
                Contact.objects.filter(user_from=request.user, user_to=user)
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'ok'})


def feedback(request):
    if request.method == 'POST':
        form = FeedbackEmailForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                send_mail(subject=cd['subject'],
                          message=cd['message'],
                          from_email=cd['sender'],
                          recipient_list=[settings.EMAIL_HOST])
            except BadHeaderError:
                return HttpResponse('Invalid header found!')
            return redirect('articles:all_articles')
    else:
        form = FeedbackEmailForm()
    return render(request, 'account/site/feedback_form.html', {'form': form})


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_next_url(request):
    next_url = request.META.get('HTTP_REFERER')
    if next_url:
        next_url = urlunquote(next_url)  # HTTP_REFERER may be encoded.
    if not is_safe_url(url=next_url, allowed_hosts=request.get_host()):
        next_url = '/'
    return next_url
