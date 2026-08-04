from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views

from users.views import CustomLoginView
from users.forms import BrevoPasswordResetForm

urlpatterns = [
    path("admin/", admin.site.urls),

    # Users App
    path("", include("users.urls")),

    # Login
    path(
        "accounts/login/",
        CustomLoginView.as_view(),
        name="login",
    ),

    # Logout
    path(
        "accounts/logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),

    # Password Reset (Using Brevo API)
    path(
        "accounts/password_reset/",
        auth_views.PasswordResetView.as_view(
            form_class=BrevoPasswordResetForm,
            template_name="registration/password_reset_form.html",
        ),
        name="password_reset",
    ),

    path(
        "accounts/password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html",
        ),
        name="password_reset_done",
    ),

    path(
        "accounts/reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html",
        ),
        name="password_reset_confirm",
    ),

    path(
        "accounts/reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),

    # Resume
    path("resume/", include("resumes.urls")),

    # Dashboard
    path("dashboard/", include("dashboard.urls")),

    # Interview
    path("interview/", include("interview.urls")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )