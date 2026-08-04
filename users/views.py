from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings

from .forms import RegisterForm
from django.contrib.auth.views import LoginView
from .forms import EmailLoginForm


class CustomLoginView(LoginView):
    template_name = "users/login.html"
    authentication_form = EmailLoginForm


def home(request):
    return render(request, "users/home.html")


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/accounts/login/")
    else:
        form = RegisterForm()

    return render(request, "users/register.html", {"form": form})


# ---------- TEMPORARY DEBUG VIEW ----------
def email_debug(request):
    return HttpResponse(f"""
    EMAIL_HOST: {settings.EMAIL_HOST}<br>
    EMAIL_PORT: {settings.EMAIL_PORT}<br>
    EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}<br>
    EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}<br>
    DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}<br>
    """)
    
    
from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings

def test_email(request):
    try:
        send_mail(
            "Render SMTP Test",
            "This email was sent from Render.",
            settings.DEFAULT_FROM_EMAIL,
            ["surekhavaitla183@gmail.com"],  # Replace with your email
            fail_silently=False,
        )
        return HttpResponse("Email sent successfully!")
    except Exception as e:
        return HttpResponse(f"Error: {type(e).__name__}<br><pre>{e}</pre>")