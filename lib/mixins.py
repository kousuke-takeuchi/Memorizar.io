from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin


class BaseMixin(LoginRequiredMixin):
    login_url = settings.LOGIN_URL