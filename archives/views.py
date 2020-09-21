from dal import autocomplete
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from articles.tagging import CustomTag, GenreTag
from archives.forms import FilmForm
from archives.models import Film


def film_list(request):
    films = Film.objects.all()
    return render(request, 'archives/film/film_list.html', {'films': films})


class AddFilm(CreateView):
    form_class = FilmForm
    template_name = 'archives/film/add_film.html'
    success_url = reverse_lazy('archives:film_list')


class TagAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # # Don't forget to filter out results depending on the visitor !
        # if not self.request.user.is_authenticated():
        #     return CustomTag.objects.none()

        qs = CustomTag.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class GenreTagAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # # Don't forget to filter out results depending on the visitor !
        # if not self.request.user.is_authenticated():
        #     return GenreTag.objects.none()

        qs = GenreTag.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs
