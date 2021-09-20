from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.contrib.auth.models import User

from lib import mixins
from . import forms


class SettingView(mixins.BaseMixin, View):
    template_name = 'users/setting.html'

    def get(self, request):
        form = forms.SettingForm()
        context = dict(form=form)
        return render(request, self.template_name, context)

    def post(self, request):
        form = forms.SettingForm(request.POST, request.FILES, context={'request': request})
        if not form.is_valid():
            context = dict(form=form)
            return render(request, self.template_name, context)
        form.save()
        return redirect('users:setting')