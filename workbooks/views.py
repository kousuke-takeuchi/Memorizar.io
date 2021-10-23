import time
import math

from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

from lib import mixins
from . import models, forms, services



class WorkbookListView(mixins.BaseMixin, View):
    template_name = 'workbooks/list.html'

    def get_querysets(self):
        workbooks = models.Workbook.objects.aggregate_training(user=self.request.user)
        p = Paginator(workbooks, 10)
        page = self.request.GET.get('page', 1)
        return p.page(page)
    
    def get(self, request):
        # 問題集一覧
        workbooks = self.get_querysets()
        form = forms.WorkbookCreateForm(context={'request': request})
        context = dict(form=form, workbooks=workbooks)
        return render(request, self.template_name, context)
    
    def post(self, request):
        # 問題集作成
        form = forms.WorkbookCreateForm(request.POST, request.FILES, context={'request': request})
        if not form.is_valid():
            workbooks = self.get_querysets()
            context = dict(form=form, workbooks=workbooks)
            return render(request, self.template_name, context)
        form.save()
        return redirect('workbooks:list')


class WorkbookImportView(mixins.BaseMixin, View):
    template_name = 'workbooks/list.html'

    def get_querysets(self):
        workbooks = models.Workbook.objects.aggregate_training(user=self.request.user)
        p = Paginator(workbooks, 10)
        page = self.request.GET.get('page', 1)
        return p.page(page)

    def post(self, request):
        # 問題集作成
        form = forms.WorkbookImportForm(request.POST, request.FILES, context={'request': request})
        if not form.is_valid():
            workbooks = self.get_querysets()
            context = dict(form=form, workbooks=workbooks)
            return render(request, self.template_name, context)
        form.save()
        return redirect('workbooks:list')


class WorkbookDetailView(mixins.BaseMixin, View):
    template_name = 'workbooks/detail.html'

    def get_querysets(self, workbook_id):
        workbook = get_object_or_404(models.Workbook, workbook_id=workbook_id)
        trainings = models.TrainingSelection.objects.aggregate(training__workbook=workbook)[:5]
        questions = workbook.question_set.all()
        p = Paginator(questions, 10)
        page = self.request.GET.get('page', 1)
        return workbook, trainings, p.page(page)
    
    def get(self, request, workbook_id):
        # 問題集の実施結果集計
        workbook, trainings, questions = self.get_querysets(workbook_id)
        service = services.WorkbookService()
        dates, learning_counts, correct_counts = service.aggregate_daily(workbook)
        context = dict(
                workbook=workbook,
                trainings=trainings,
                questions=questions,
                dates=dates,
                learning_counts=learning_counts,
                correct_counts=correct_counts,
            )
        return render(request, self.template_name, context)
    
    def post(self, request, workbook_id):
        # トレーニングを開始する
        workbook = get_object_or_404(models.Workbook, workbook_id=workbook_id)
        form = forms.WorkbookTrainingCreateForm(request.POST, context={'request': request, 'workbook': workbook})
        if not form.is_valid():
            workbook, trainings, questions = self.get_querysets(workbook_id)
            service = services.WorkbookService()
            dates, learning_counts, correct_counts = service.aggregate_daily(workbook)
            context = dict(
                workbook=workbook,
                trainings=trainings,
                questions=questions,
                dates=dates,
                learning_counts=learning_counts,
                correct_counts=correct_counts,
            )
            return render(request, self.template_name, context)
        training = form.save()
        return redirect('workbooks:training_question', workbook_id=training.workbook.workbook_id, training_id=training.training_id)


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


class WorkbookDeleteView(mixins.BaseMixin, View):
    def get_querysets(self, workbook_id):
        workbook = get_object_or_404(models.Workbook, workbook_id=workbook_id)
        return workbook
    
    def post(self, _, workbook_id):
        workbook = self.get_querysets(workbook_id)
        workbook.delete()
        return redirect('workbooks:list')


class QuestionCreateView(mixins.BaseMixin, View):
    template_name = 'workbooks/questions/new.html'

    def get_querysets(self, workbook_id):
        workbook = get_object_or_404(models.Workbook, workbook_id=workbook_id)
        return workbook
    
    def get_question(self, question_id):
        if question_id is None:
            return None
        return get_object_or_404(models.Question, question_id=question_id)
    
    def get(self, request, workbook_id):
        workbook = self.get_querysets(workbook_id)
        # question_idが指定されている場合は、問題を複製
        original_question = self.get_question(request.GET.get('question_id'))
        form = forms.QuestionCreateForm()
        context = dict(original_question=original_question, workbook=workbook, form=form)
        return render(request, self.template_name, context)
    
    def post(self, request, workbook_id):
        workbook = self.get_querysets(workbook_id)
        form = forms.QuestionCreateForm(request.POST, request.FILES, context={'request': request, 'workbook': workbook})
        if not form.is_valid():
            context = dict(workbook=workbook, form=form)
            return render(request, self.template_name, context)
        form.save()
        return redirect('workbooks:detail', workbook_id=workbook.workbook_id)


class QuestionEditView(mixins.BaseMixin, View):
    template_name = 'workbooks/questions/edit.html'

    def get_querysets(self, workbook_id, question_id):
        question = get_object_or_404(models.Question, workbook__workbook_id=workbook_id, question_id=question_id)
        return question
    
    def get(self, request, workbook_id, question_id):
        question = self.get_querysets(workbook_id, question_id)
        form = forms.QuestionUpdateForm()
        context = dict(workbook=question.workbook, question=question, form=form)
        return render(request, self.template_name, context)
    
    def post(self, request, workbook_id, question_id):
        question = self.get_querysets(workbook_id, question_id)
        form = forms.QuestionUpdateForm(request.POST, request.FILES, context={'request': request, 'question': question, 'workbook': question.workbook})
        if not form.is_valid():
            context = dict(question=question, form=form, workbook=question.workbook)
            return render(request, self.template_name, context)
        form.save()
        return redirect('workbooks:detail', workbook_id=question.workbook.workbook_id)


class QuestionDeleteView(mixins.BaseMixin, View):
    def get_querysets(self, workbook_id, question_id):
        question = get_object_or_404(models.Question, workbook__workbook_id=workbook_id, question_id=question_id)
        return question
    
    def post(self, request, workbook_id, question_id):
        question = self.get_querysets(workbook_id, question_id)
        question.delete()
        return redirect('workbooks:detail', workbook_id=workbook_id)


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


class ChapterEditView(mixins.BaseMixin, View):
    template_name = 'workbooks/chapters/edit.html'

    def get_querysets(self, workbook_id, chapter_id):
        chapter = get_object_or_404(models.Chapter, workbook__workbook_id=workbook_id, chapter_id=chapter_id)
        return chapter
    
    def get(self, request, workbook_id, chapter_id):
        chapter = self.get_querysets(workbook_id, chapter_id)
        form = forms.ChapterUpdateForm()
        context = dict(workbook=chapter.workbook, chapter=chapter, form=form)
        return render(request, self.template_name, context)
    
    def post(self, request, workbook_id, chapter_id):
        chapter = self.get_querysets(workbook_id, chapter_id)
        form = forms.ChapterUpdateForm(request.POST, context={'request': request, 'chapter': chapter})
        if not form.is_valid():
            context = dict(workbook=chapter.workbook, chapter=chapter, form=form)
            return render(request, self.template_name, context)
        form.save()
        return redirect('workbooks:detail', workbook_id=chapter.workbook.workbook_id)


class ChapterDeleteView(mixins.BaseMixin, View):
    def get_querysets(self, workbook_id, chapter_id):
        chapter = get_object_or_404(models.Chapter, workbook__workbook_id=workbook_id, chapter_id=chapter_id)
        return chapter
    
    def post(self, request, workbook_id, chapter_id):
        chapter = self.get_querysets(workbook_id, chapter_id)
        chapter.delete()
        return redirect('workbooks:detail', workbook_id=workbook_id)


class WorkbookTrainingSelectChapterView(mixins.BaseMixin, View):
    template_name = 'workbooks/trainings/select_chapter.html'

    def get_querysets(self, workbook_id):
        workbook = get_object_or_404(models.Workbook, workbook_id=workbook_id)
        return workbook
    
    # チャプター一覧を表示
    def get(self, request, workbook_id):
        workbook = self.get_querysets(workbook_id)
        chapters = models.Chapter.objects.filter(workbook=workbook)
        form = forms.WorkbookTrainingSelectChapterForm(context={'request': request})
        context = dict(form=form, chapters=chapters)
        return render(request, self.template_name, context)
    
    # チャプターを関連付けて問題を開始
    def post(self, request, workbook_id):
        workbook = self.get_querysets(workbook_id)

        form = forms.WorkbookTrainingSelectChapterForm(request.POST, context={'request': request, 'workbook': workbook})
        if not form.is_valid():
            chapters = models.Chapter.objects.filter(workbook=workbook)
            context = dict(form=form, chapters=chapters)
            return render(request, self.template_name, context)
        training = form.save()
        # 問題ページに移動
        return redirect('workbooks:training_question', training_id=training.training_id)


class WorkbookTrainingQuestionView(mixins.BaseMixin, View):
    template_name = 'workbooks/trainings/question.html'
    not_found_template_name = 'workbooks/trainings/question_not_found.html'
    
    # 問題を表示
    def get(self, request, workbook_id, training_id):
        training = get_object_or_404(models.Training, training_id=training_id)

        # もし終了している場合は結果ページへ
        if training.done:
            return redirect('workbooks:training_result', training_id=training.training_id)

        service = services.TrainingService()

        # 表示する問題がない場合は、問題がありませんのページへ
        if service.did_finish(training):
            context = {}
            return render(request, self.not_found_template_name, context)
        
        # 問題集から次の問題と回答選択肢を選ぶ
        question, answers = service.select_question(training)

        form = forms.WorkbookTrainingQuestionForm(context={'request': request})
        context = dict(form=form, question=question, answers=answers, start_at=time.time())
        return render(request, self.template_name, context)
    
    # 回答を送信
    def post(self, request, workbook_id, training_id):
        training = get_object_or_404(models.Training, training_id=training_id)

        form = forms.WorkbookTrainingQuestionForm(request.POST, context={'request': request, 'training': training})
        if not form.is_valid():
            context = dict(form=form)
            return render(request, self.template_name, context)
        training_selection = form.save()

        # 10問解いたら終了
        service = services.TrainingService()
        if service.did_finish(training):
            training.done = True
            training.save()

        # 正答結果ページに移動
        return redirect('workbooks:training_answer', training_id=training.training_id, selection_id=training_selection.training_selection_id)


class WorkbookTrainingAnswerView(mixins.BaseMixin, View):
    template_name = 'workbooks/trainings/answer.html'
    
    def get(self, request, workbook_id, training_id, selection_id):
        training_selection = get_object_or_404(models.TrainingSelection, training_selection_id=selection_id)
        answers = models.Answer.objects.filter(question=training_selection.question)

        context = dict(training_selection=training_selection, answers=answers)
        return render(request, self.template_name, context)


class WorkbookTrainingResultView(mixins.BaseMixin, View):
    template_name = 'workbooks/trainings/result.html'
    
    def get(self, request, workbook_id, training_id):
        training = get_object_or_404(models.Training, training_id=training_id, done=True)

        # 正解数/回答数
        selection_count = models.TrainingSelection.objects.filter(training=training).count()
        true_count = models.TrainingSelection.objects.filter(training=training, correct=True).count()
        true_rate = math.floor(100 * true_count / selection_count)

        context = dict(training=training, selection_count=selection_count, true_count=true_count, true_rate=true_rate)
        return render(request, self.template_name, context)