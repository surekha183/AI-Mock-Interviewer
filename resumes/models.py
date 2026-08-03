from django.db import models
from django.contrib.auth.models import User


class Resume(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    resume = models.FileField(
        upload_to="resumes/"
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    extracted_text = models.TextField(
        blank=True
    )

    skills = models.TextField(blank=True)

    projects = models.TextField(blank=True)

    education = models.TextField(blank=True)

    certifications = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} Resume"