from django.urls import path, include
from .views import *
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    path('', home, name='home'),
    path('login/', LoginView.as_view(template_name="users/auth/login.html"), name='login'),
    path('logout/', LogoutView.as_view(template_name="users/auth/logout.html"), name='logout'),

    path('profile', profile, name='profile'),
    path('school_profile', school_profile, name='school_profile'),
    path('staff_profile', staff_profile, name='staff_profile'),

    path(
        'reset_password/',
        PasswordResetView.as_view(template_name="users/auth/password_reset.html"),
        name='reset_password'
    ),
    path(
        'reset_password/done',
        PasswordResetDoneView.as_view(template_name="users/auth/password_reset_done.html"),
        name='password_reset_done'
    ),
    path(
        'password-reset-confirm/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(template_name="users/auth/password_reset_confirm.html"),
        name='password_reset_confirm'
    ),
    path(
        'password-reset-complete',
        PasswordResetCompleteView.as_view(template_name="users/auth/password_reset_complete.html"),
        name='password_reset_complete'
    ),

    path('register/', SignUpView.as_view(), name='register'),
    path('signup/', register, name='signup'),
    path('password_change/', change_password, name='change_password'),

    path('users-list/', UserListView.as_view(), name='users-list'),
    path('admin-list/', AdminListView.as_view(), name='admins-list')

]
