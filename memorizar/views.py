from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.conf import settings


class DashboardView(View):
    template_name = 'memorizar/index.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect(settings.LOGIN_URL)
        context = dict()
        return render(request, self.template_name, context)