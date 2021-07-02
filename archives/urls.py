from django.urls import path
from . import views

app_name = "archives"
urlpatterns = [
    path("films/", views.film_list, name="film_list"),
]
