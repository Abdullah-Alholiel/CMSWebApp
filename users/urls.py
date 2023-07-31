from . import views
from django.urls import path
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("register/", views.register, name="register"),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="users/logout.html"),
        name="logout",
    ),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="users/login.html"),
        name="login",
    ),
    path("accounts/profile/", views.profile, name="profile"),
    # custom password reset views
    path(
        "password-reset",
        views.CustomPasswordResetView.as_view(),
        name="custom_password_reset",
    ),
    path(
        "password-reset/sent",
        views.CustomPasswordResetSentView.as_view(),
        name="custom_password_reset_sent",
    ),
    path(
        "password-reset/confirm/<uidb64>/<token>",
        views.CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password-reset/complete",
        views.CustomPasswordResetCompleteView.as_view(),
        name="custom_password_reset_complete",
    ),
]
