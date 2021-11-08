from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.base import View
from django.core.paginator import Paginator

from lib import mixins
from workbooks import models
from . import forms


class WorkbookSearchView(mixins.BaseMixin, View):
    template_name = 'socials/list.html'

    def get_querysets(self):
        workbooks = models.Workbook.objects.search(keyword=self.request.GET.get('keyword'))
        p = Paginator(workbooks, 9)
        page = self.request.GET.get('page', 1)
        return p.page(page)
    
    def get(self, request):
        # 問題集一覧
        workbooks = self.get_querysets()
        categories = models.Category.objects.all()
        context = dict(workbooks=workbooks, categories=categories)
        return render(request, self.template_name, context)


class WorkbookRegistrationView(mixins.BaseMixin, View):
    def get_querysets(self, workbook_id):
        workbook = get_object_or_404(models.Workbook, workbook_id=workbook_id)
        return workbook
    
    def post(self, request, workbook_id):
        # 問題集をマイページに登録
        workbook = self.get_querysets(workbook_id)
        models.Registration.objects.create(user=request.user, workbook=workbook)
        return redirect('workbooks:list')