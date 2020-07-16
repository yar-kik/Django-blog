from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile

def user_login(request):
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
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})


def register(request):
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
                return render(request, 'account/register_done.html',
                              {'new_user': new_user})
        else:
            user_form = UserRegistrationForm()
        return render(request, 'account/register.html',
                      {'user_form': user_form})


@login_required
def edit(request):
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
