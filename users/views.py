from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout
from django.core.paginator import Paginator

from lib import mixins
from . import forms, services


class UserEditView(mixins.BaseMixin, View):
    template_name = 'users/edit.html'

    def get_querysets(self, user_id):
        querysets = get_object_or_404(models.User, user_id=user_id)
        return querysets

    def get(self, request, user_id):
        user = self.get_querysets(user_id)
        form = forms.UserEditForm()
        context = dict(user=user, form=form)
        return render(request, self.template_name, context)

    def post(self, request, user_id):
        user = self.get_querysets(user_id)
        form = forms.UserEditForm(request.POST, request.FILES, context={'request': request, 'user': user})
        if not form.is_valid():
            context = dict(user=user, form=form)
            return render(request, self.template_name, context)
        user = form.save()
        return redirect('users:list')