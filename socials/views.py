from django.shortcuts import render
from django.views.generic.base import View
from django.core.paginator import Paginator

from lib import mixins
from workbooks import models


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