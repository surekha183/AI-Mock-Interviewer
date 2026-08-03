from django.contrib import admin

from .models import (
    InterviewSession,
    Conversation,
    InterviewReport,
)

admin.site.register(InterviewSession)
admin.site.register(Conversation)
admin.site.register(InterviewReport)