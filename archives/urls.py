from django.urls import path
from . import views
from .views import TagAutocomplete, GenreTagAutocomplete

app_name = 'archives'
urlpatterns = [
    path('tag_autocomplete/', TagAutocomplete.as_view(), name='tag_autocomplete'),
    path('genre_autocomplete/', GenreTagAutocomplete.as_view(), name='genre_autocomplete'),
    path('films/', views.film_list, name='film_list'),
    path('films/add_new/', views.AddFilm.as_view(), name='add_film'),
]