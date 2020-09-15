from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views  # щоб не було конфлікту імен
from . import views

app_name = 'account'
urlpatterns = [
    # path('login/', views.user_login, name='login'),
    path('', views.dashboard, name='dashboard'),
    # Для уточнення місцезнаходження шаблона
    # path('login/', auth_views.LoginView.as_view(template_name='account/registration/login.html'), name='login'),
    path('feedback/', views.feedback, name='feedback'),
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True),
         name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(),
         name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        success_url=reverse_lazy('account:password_reset_done')),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordChangeDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        success_url=reverse_lazy('account:password_reset_complete')),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('users/', views.user_list, name='user_list'),
    path('users/follow/', views.user_follow, name='user_follow'),
    path('users/<username>/', views.user_detail, name='user_detail'),
]
