from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.http import Http404, JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

from lib import mixins
from . import models, services



class DiagnosisCreateView(mixins.BaseMixin, View):
    template_name = 'diagnoses/create.html'
    
    def get(self, request):
        context = dict(user_id=request.user.user_id)
        return render(request, self.template_name, context)