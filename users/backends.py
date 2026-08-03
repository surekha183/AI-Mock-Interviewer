from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


class EmailBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):

        email = username

        user = User.objects.filter(email=email).first()

        if user is None:
            return None

        if user.check_password(password):
            return user

        return None