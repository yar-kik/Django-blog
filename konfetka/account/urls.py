from django.urls import path
from django.contrib.auth import views as auth_views  # щоб не було конфлікту імен
from . import views

app_name = 'account'
urlpatterns = [
    # path('login/', views.user_login, name='login'),
    path('', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='account/registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='account/registration/logged_out.html'), name='logout'),
]
