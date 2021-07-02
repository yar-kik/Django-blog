from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from archives.forms import FilmForm
from archives.models import Film


def film_list(request):
    films = Film.objects.all()
    return render(request, "archives/film/film_list.html", {"films": films})


class AddFilm(CreateView):
    form_class = FilmForm
    template_name = "archives/film/add_film.html"
    success_url = reverse_lazy("archives:film_list")
