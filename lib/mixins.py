from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework.permissions import IsAuthenticated

from . import auth


class BaseMixin(LoginRequiredMixin):
    login_url = settings.LOGIN_URL


class MemorizarBaseMixin:
    authentication_classes = [auth.MemorizarBaseAuthenication]
    permission_classes = [IsAuthenticated]