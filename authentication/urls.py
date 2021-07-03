"""Module for auth urls"""

from django.urls import path

from authentication.views import RegistrationApiView, LoginApiView

# pylint: disable=invalid-name
app_name = "auth"
urlpatterns = [
    path("registration/", RegistrationApiView.as_view()),
    path("login/", LoginApiView.as_view()),
]
