from django.contrib.auth.backends import ModelBackend
from .models import Volunteer
from django.contrib.auth.hashers import check_password


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Volunteer.objects.get(email=username)
        except Volunteer.DoesNotExist:
            return None

        if check_password(password, user.password):
            return user
        return None
