import time
import math

from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.http import Http404, HttpResponse
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

from lib import mixins
from . import models, forms, services



class WorkbookListView(mixins.BaseMixin, View):
    template_name = 'workbooks/list.html'

    def get_querysets(self):
        workbooks = models.Workbook.objects.aggregate_training(user=self.request.user)
        return workbooks
    
    def get(self, request):
        # 問題集一覧
        querysets = self.get_querysets()
        form = forms.WorkbookCreateForm(context={'request': request})
        context = dict(form=form, page_obj=querysets)
        return render(request, self.template_name, context)
    
    def post(self, request):
        # 問題集作成
        form = forms.WorkbookCreateForm(request.POST, request.FILES, context={'request': request})
        if not form.is_valid():
            context = dict(form=form)
            return render(request, self.template_name, context)
        form.save()
        return redirect('workbooks:list')


class WorkbookDetailView(mixins.BaseMixin, View):
    template_name = 'workbooks/detail.html'

    def get_querysets(self, workbook_id):
        workbook = get_object_or_404(models.Workbook, workbook_id=workbook_id)
        querysets = models.TrainingSelection.objects.aggregate(training__workbook=workbook)
        return workbook, querysets
    
    def get(self, request, workbook_id):
        # 問題集の実施結果集計
        workbook, trainings = self.get_querysets(workbook_id)
        context = dict(workbook=workbook, page_obj=trainings)
        return render(request, self.template_name, context)
    
    def post(self, request, workbook_id):
        # トレーニングを開始する
        workbook = get_object_or_404(models.Workbook, workbook_id=workbook_id)
        training = models.Training.objects.create(workbook=workbook, user=request.user)
        return redirect('workbooks:training_question', training_id=training.training_id)


class WorkbookCreateView(mixins.BaseMixin, View):
    template_name = 'workbooks/new.html'
    
    def get(self, request):
        form = forms.WorkbookCreateForm()
        context = dict(form=form)
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = forms.WorkbookCreateForm(request.POST, context={'request': request})
        if not form.is_valid():
            context = dict(form=form)
            return render(request, self.template_name, context)
        workbook = form.save()
        return redirect('workbooks:detail', workbook_id=workbook.workbook_id)


class WorkbookEditView(mixins.BaseMixin, View):
    template_name = 'workbooks/edit.html'

    def get_querysets(self, workbook_id):
        workbook = get_object_or_404(models.Workbook, workbook_id=workbook_id)
        return workbook
    
    def get(self, request, workbook_id):
        workbook = self.get_querysets(workbook_id)
        form = forms.WorkbookUpdateForm()
        context = dict(workbook=workbook, form=form)
        return render(request, self.template_name, context)
    
    def post(self, request, workbook_id):
        workbook = self.get_querysets(workbook_id)
        form = forms.WorkbookUpdateForm(request.POST, context={'request': request, 'workbook': workbook})
        if not form.is_valid():
            context = dict(workbook=workbook, form=form)
            return render(request, self.template_name, context)
        workbook = form.save()
        return redirect('workbooks:detail', workbook_id=workbook.workbook_id)


class QuestionCreateView(mixins.BaseMixin, View):
    template_name = 'workbooks/questions/new.html'

    def get_querysets(self, workbook_id):
        workbook = get_object_or_404(models.Workbook, workbook_id=workbook_id)
        return workbook
    
    def get(self, request, workbook_id):
        workbook = self.get_querysets(workbook_id)
        form = forms.QuestionCreateForm()
        context = dict(workbook=workbook, form=form)
        return render(request, self.template_name, context)
    
    def post(self, request, workbook_id):
        workbook = self.get_querysets(workbook_id)
        form = forms.QuestionCreateForm(request.POST, context={'request': request, 'workbook': workbook})
        if not form.is_valid():
            context = dict(workbook=workbook, form=form)
            return render(request, self.template_name, context)
        form.save()
        return redirect('workbooks:detail', workbook_id=workbook.workbook_id)


class ChapterCreateView(mixins.BaseMixin, View):
    template_name = 'workbooks/chapters/new.html'

    def get_querysets(self, workbook_id):
        workbook = get_object_or_404(models.Workbook, workbook_id=workbook_id)
        return workbook
    
    def get(self, request, workbook_id):
        workbook = self.get_querysets(workbook_id)
        form = forms.ChapterCreateForm()
        context = dict(workbook=workbook, form=form)
        return render(request, self.template_name, context)
    
    def post(self, request, workbook_id):
        workbook = self.get_querysets(workbook_id)
        form = forms.ChapterCreateForm(request.POST, context={'request': request, 'workbook': workbook})
        if not form.is_valid():
            context = dict(workbook=workbook, form=form)
            return render(request, self.template_name, context)
        form.save()
        return redirect('workbooks:detail', workbook_id=workbook.workbook_id)


class WorkbookTrainingQuestionView(mixins.BaseMixin, View):
    template_name = 'workbooks/trainings/question.html'
    
    # 問題を表示
    def get(self, request, training_id):
        training = get_object_or_404(models.Training, training_id=training_id)

        # もし終了している場合は結果ページへ
        if training.done:
            return redirect('workbooks:training_result', training_id=training.training_id)

        # 問題集に含まれる問題の中から、ランダムに問題を取得する
        question = models.Question.objects.filter(workbook=training.workbook).order_by('?').first()
        answers = models.Answer.objects.filter(question=question)

        form = forms.WorkbookTrainingQuestionForm(context={'request': request})
        context = dict(form=form, question=question, answers=answers, start_at=time.time())
        return render(request, self.template_name, context)
    
    # 回答を送信
    def post(self, request, training_id):
        training = get_object_or_404(models.Training, training_id=training_id)

        form = forms.WorkbookTrainingQuestionForm(request.POST, context={'request': request, 'training': training})
        if not form.is_valid():
            context = dict(form=form)
            return render(request, self.template_name, context)
        training_selection = form.save()

        # 10問解いたら終了
        if len(models.TrainingSelection.objects.filter(training=training)) >= 10:
            training.done = True
            training.save()

        # 正答結果ページに移動
        return redirect('workbooks:training_answer', training_id=training.training_id, selection_id=training_selection.training_selection_id)


class WorkbookTrainingAnswerView(mixins.BaseMixin, View):
    template_name = 'workbooks/trainings/answer.html'
    
    def get(self, request, training_id, selection_id):
        training_selection = get_object_or_404(models.TrainingSelection, training_selection_id=selection_id)
        answers = models.Answer.objects.filter(question=training_selection.question)

        context = dict(training_selection=training_selection, answers=answers)
        return render(request, self.template_name, context)


class WorkbookTrainingResultView(mixins.BaseMixin, View):
    template_name = 'workbooks/trainings/result.html'
    
    def get(self, request, training_id):
        training = get_object_or_404(models.Training, training_id=training_id, done=True)

        # 正解数/回答数
        selection_count = models.TrainingSelection.objects.filter(training=training).count()
        true_count = models.TrainingSelection.objects.filter(training=training, correct=True).count()
        true_rate = math.floor(100 * true_count / selection_count)

        context = dict(selection_count=selection_count, true_count=true_count, true_rate=true_rate)
        return render(request, self.template_name, context)