from django.urls import path

from . import views

urlpatterns = [

    # Select role
    path(
        "",
        views.role_selection,
        name="interview_home"
    ),

    # Voice interview page
    path(
        "<int:interview_id>/",
        views.voice_interview,
        name="voice_interview"
    ),

    # Receive user's answer
    path(
        "<int:interview_id>/respond/",
        views.respond,
        name="respond"
    ),

    # Interview report page
    path(
        "report/<int:interview_id>/",
        views.interview_report,
        name="interview_report"
    ),

    # Previous reports
    path(
        "reports/",
        views.previous_reports,
        name="previous_reports"
    ),
    
    path(
        "profile/",
        views.profile,
        name="profile"
),

]