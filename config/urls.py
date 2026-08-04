from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views
from users.views import CustomLoginView

from users.views import CustomLoginView, email_debug, test_email


urlpatterns = [
    path("admin/", admin.site.urls),
    
    path("debug-email/", email_debug),
    
    path("test-email/", test_email),

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

    # Password Reset
    path(
        "accounts/password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset_form.html",
            email_template_name="registration/password_reset_email.html",
            subject_template_name="registration/password_reset_subject.txt",
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