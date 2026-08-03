from django.db import models
from django.contrib.auth.models import User


class InterviewSession(models.Model):

    ROLE_CHOICES = [
        ("Python Developer", "Python Developer"),
        ("Data Analyst", "Data Analyst"),
        ("Software Engineer", "Software Engineer"),
        ("Django Developer", "Django Developer"),
        ("SQL Developer", "SQL Developer"),
    ]

    EXPERIENCE_CHOICES = [
        ("Fresher", "Fresher"),
        ("1-2 Years", "1-2 Years"),
        ("3-5 Years", "3-5 Years"),
    ]

    STATUS_CHOICES = [
        ("Started", "Started"),
        ("Completed", "Completed"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="interviews"
    )

    role = models.CharField(
        max_length=100,
        choices=ROLE_CHOICES
    )

    experience = models.CharField(
        max_length=50,
        choices=EXPERIENCE_CHOICES
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Started"
    )

    question_count = models.IntegerField(
        default=0
    )

    started_at = models.DateTimeField(
        auto_now_add=True
    )

    ended_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):

        return f"{self.user.username} - {self.role}"


class Conversation(models.Model):

    SPEAKER_CHOICES = [
        ("AI", "AI"),
        ("USER", "USER"),
    ]

    interview = models.ForeignKey(
        InterviewSession,
        on_delete=models.CASCADE,
        related_name="messages"
    )

    speaker = models.CharField(
        max_length=10,
        choices=SPEAKER_CHOICES
    )

    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = ["created_at"]

    def __str__(self):

        return f"{self.speaker}: {self.message[:40]}"
    
    
class AnswerEvaluation(models.Model):

    conversation = models.OneToOneField(
        Conversation,
        on_delete=models.CASCADE,
        related_name="evaluation"
    )

    technical_score = models.IntegerField(default=0)

    communication_score = models.IntegerField(default=0)

    confidence_score = models.IntegerField(default=0)

    feedback = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Evaluation {self.conversation.id}"


class InterviewReport(models.Model):

    interview = models.OneToOneField(
        InterviewSession,
        on_delete=models.CASCADE,
        related_name="report"
    )

    overall_score = models.IntegerField(
        default=0
    )

    technical_score = models.IntegerField(
        default=0
    )

    communication_score = models.IntegerField(
        default=0
    )

    confidence_score = models.IntegerField(
        default=0
    )

    strengths = models.TextField(
        blank=True
    )

    weaknesses = models.TextField(
        blank=True
    )

    suggestions = models.TextField(
        blank=True
    )

    generated_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"Report - {self.interview.user.username}"