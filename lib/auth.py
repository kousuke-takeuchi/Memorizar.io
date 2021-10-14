from django.contrib.auth.models import User

from rest_framework import authentication
from rest_framework import exceptions


def authorize(request):
    authorization = request.META.get('HTTP_X_AUTHORIZATION', '')
    if not authorization:
        authorization = request.META.get('HTTP_AUTHORIZATION', '')
    user_id = authorization.replace('Token', '').strip()
    if not user_id:
        raise exceptions.AuthenticationFailed('認証トークンを指定してください')
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise exceptions.AuthenticationFailed('ユーザーが存在しません')
    if not user.is_active:
        raise exceptions.AuthenticationFailed('無効なトークンです')
    return user


class MemorizarBaseAuthenication(authentication.BaseAuthentication):
    def authenticate(self, request):
        user = authorize(request)
        return (user, None)


class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.process_request(request)
        response = self.get_response(request)
        self.process_response(request, response)
        return response

    def process_request(self, request):
        try:
            user = authorize(request)
        except exceptions.AuthenticationFailed:
            return
        request.user = user

    def process_response(self, request, response):
        pass