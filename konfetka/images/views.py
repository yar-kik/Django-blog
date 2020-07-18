from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm


@login_required
def image_create(request):
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
            messages.success(request, 'Image added successfully')
            """Перенаправляємо користувача на сторінку збереженого зображення"""
            return redirect(new_item.get_absolute_url())
    else:
        """Заповнюємо форму із GET-запиту"""
        form = ImageCreateForm(data=request.GET)
    return render(request, 'images/image/create.html',
                  {'section': 'images', 'form': form})
