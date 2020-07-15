from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm


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
