from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView

from .forms import RegisterForm, EmailLoginForm


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