import os
import uuid
import zipfile
import time

import openpyxl

from django import forms
from django.contrib.auth import authenticate, login
from django.core.validators import MinLengthValidator
from django.templatetags.static import static

from . import models, services
import workbooks


class WorkbookCreateForm(forms.Form):
    workbook_file = forms.FileField(required=True)

    def __init__(self, *args, **kwargs):
        self.context = kwargs.pop('context', {})
        super(WorkbookCreateForm, self).__init__(*args, **kwargs)
    
    def clean_workbook_file(self):
        workbook_file = self.cleaned_data.get('workbook_file')
        filename = 'tmp/{}.xlsx'.format(uuid.uuid4())
        with open(filename, 'wb+') as f:
            f.write(workbook_file.read())
        try:
            wb = openpyxl.load_workbook(filename)
        except zipfile.BadZipFile:
            os.remove(filename)
            raise forms.ValidationError('Excelファイルを指定してください')
        return filename

    def save(self):
        filename = self.cleaned_data.get('workbook_file')
        service = services.WorkbookService()
        service.import_workbook(self.context['request'].user, filename)
        os.remove(filename)


class WorkbookCreateForm(forms.Form):
    title = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        self.context = kwargs.pop('context', {})
        super(WorkbookCreateForm, self).__init__(*args, **kwargs)

    def save(self):
        workbook = models.Workbook.objects.create(
            user=self.context['request'].user,
            title=self.cleaned_data.get('title'),
        )
        return workbook


class WorkbookUpdateForm(forms.Form):
    title = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        self.context = kwargs.pop('context', {})
        super(WorkbookUpdateForm, self).__init__(*args, **kwargs)

    def save(self):
        workbook = self.context['workbook']
        workbook.title = self.cleaned_data.get('title')
        workbook.save()
        return workbook


class QuestionCreateForm(forms.Form):
    question_id = forms.CharField(required=True)
    title = forms.CharField(required=True)
    sentense = forms.CharField(required=True)
    chapter_id = forms.CharField(required=False)
    image = forms.FileField(required=False)
    answer1_title = forms.CharField(required=True)
    answer1_sentense = forms.CharField(required=True)
    answer2_title = forms.CharField(required=True)
    answer2_sentense = forms.CharField(required=True)
    answer3_title = forms.CharField(required=True)
    answer3_sentense = forms.CharField(required=True)
    answer4_title = forms.CharField(required=True)
    answer4_sentense = forms.CharField(required=True)
    collect_index = forms.IntegerField(required=True)
    commentary = forms.CharField(required=True)
    commentary_image = forms.FileField(required=False)

    def __init__(self, *args, **kwargs):
        self.context = kwargs.pop('context', {})
        super(QuestionCreateForm, self).__init__(*args, **kwargs)
    
    def clean_chapter_id(self):
        chapter_id = self.cleaned_data.get('chapter_id')
        if chapter_id:
            try:
                chapter = models.Chapter.objects.get(chapter_id=chapter_id, workbook=self.context['workbook'])
            except models.Chapter.DoesNotExist:
                raise forms.ValidationError('このIDは存在しません')
        return chapter

    def create_answer(self, question, index):
        answer = models.Answer.objects.create(
            question=question,
            title=self.cleaned_data.get('answer{}_title'.format(index)),
            sentense=self.cleaned_data.get('answer{}_sentense'.format(index)),
            is_true=self.cleaned_data.get('collect_index') == index,
        )
        return answer

    def save(self):
        question = models.Question.objects.create(
            workbook=self.context['workbook'],
            question_id=self.cleaned_data.get('question_id'),
            title=self.cleaned_data.get('title'),
            sentense=self.cleaned_data.get('sentense'),
            chapter=self.cleaned_data.get('chapter_id'),
            commentary=self.cleaned_data.get('commentary'),
        )
        self.create_answer(question, 1)
        self.create_answer(question, 2)
        self.create_answer(question, 3)
        self.create_answer(question, 4)
        return question


class ChapterCreateForm(forms.Form):
    chapter_id = forms.CharField(required=True)
    title = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        self.context = kwargs.pop('context', {})
        super(ChapterCreateForm, self).__init__(*args, **kwargs)

    def save(self):
        chapter = models.Chapter.objects.create(
            workbook=self.context['workbook'],
            chapter_id=self.cleaned_data.get('chapter_id'),
            title=self.cleaned_data.get('title'),
        )
        return chapter


class WorkbookTrainingQuestionForm(forms.Form):
    selected_id = forms.CharField(required=True)
    question_id = forms.CharField(required=True)
    start_at = forms.FloatField(required=True)

    def __init__(self, *args, **kwargs):
        self.context = kwargs.pop('context', {})
        super(WorkbookTrainingQuestionForm, self).__init__(*args, **kwargs)

    def clean_selected_id(self):
        selected_id = self.cleaned_data.get('selected_id')
        try:
            answer = models.Answer.objects.get(answer_id=selected_id)
        except models.Answer.DoesNotExist:
            raise forms.ValidationError('invalid selected_id')
        return answer

    def clean_question_id(self):
        question_id = self.cleaned_data.get('question_id')
        try:
            question = models.Question.objects.get(question_id=question_id)
        except models.Question.DoesNotExist:
            raise forms.ValidationError('invalid question_id')
        return question

    def save(self):
        selection = models.TrainingSelection.objects.create(
            training=self.context['training'],
            question=self.cleaned_data['question_id'],
            answer=self.cleaned_data['selected_id'],
            correct=self.cleaned_data['selected_id'].is_true,
            duration=time.time() - self.cleaned_data['start_at'],
        )
        return selection