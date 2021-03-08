from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin


class BaseMixin(LoginRequiredMixin):
    pass