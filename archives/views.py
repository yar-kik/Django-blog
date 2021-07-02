from django.shortcuts import render
from archives.models import Film


def film_list(request):
    films = Film.objects.all()
    return render(request, "archives/film/film_list.html", {"films": films})

