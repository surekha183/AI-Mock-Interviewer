from django.urls import path
from . import views
from .views import CustomLoginView

urlpatterns = [

    path("", views.home, name="home"),

    path("register/", views.register, name="register"),

    path("login/", CustomLoginView.as_view(), name="login"),

]