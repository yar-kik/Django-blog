from django.urls import path
from django.contrib.auth import views as auth_views  # щоб не було конфлікту імен
from . import views

app_name = 'account'
urlpatterns = [
    # path('login/', views.user_login, name='login'),
    path('', views.dashboard, name='dashboard'),
    # Для уточнення місцезнаходження шаблона
    # path('login/', auth_views.LoginView.as_view(template_name='account/registration/login.html'), name='login'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
]
