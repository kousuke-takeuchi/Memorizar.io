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