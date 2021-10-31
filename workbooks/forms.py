import os
import uuid
import zipfile
import time

import openpyxl

from django import forms
from django.core.files.storage import default_storage
from multivaluefield import MultiValueField

from . import models, tasks


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


class WorkbookImportForm(forms.Form):
    title = forms.CharField(required=True)
    workbook_file = forms.FileField(required=True)

    def __init__(self, *args, **kwargs):
        self.context = kwargs.pop('context', {})
        super(WorkbookImportForm, self).__init__(*args, **kwargs)

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if models.Workbook.objects.filter(title=title).exists():
            raise forms.ValidationError('この名前はすでに使用されています')
        return title
    
    def clean_workbook_file(self):
        workbook_file = self.cleaned_data.get('workbook_file')
        filename = 'tmp/{}.xlsx'.format(uuid.uuid4())
        with open(filename, 'wb+') as f:
            f.write(workbook_file.read())
        try:
            openpyxl.load_workbook(filename)
        except zipfile.BadZipFile:
            os.remove(filename)
            raise forms.ValidationError('Excelファイルを指定してください')
        return os.path.abspath(filename)

    def save(self):
        title = self.cleaned_data.get('title')
        file_path = self.cleaned_data.get('workbook_file')
        # インポート処理をバックグラウンドで開始
        user_id = self.context['request'].user.id
        tasks.import_workbook_task.delay(user_id, title, file_path)


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

    def upload(self, image_file):
        file_name = default_storage.save(image_file.name, image_file)
        return default_storage.url(file_name)

    def save(self):
        # 画像をアップロード
        image_file = self.cleaned_data['image']
        image_urls = []
        if image_file:
            image_url = self.upload(image_file)
            image_urls.append(image_url)
        
        commentary_image_file = self.cleaned_data['commentary_image']
        commentary_image_urls = []
        if image_file:
            commentary_image_url = self.upload(commentary_image_file)
            commentary_image_urls.append(commentary_image_url)
        
        question = models.Question.objects.create(
            workbook=self.context['workbook'],
            title=self.cleaned_data.get('title'),
            sentense=self.cleaned_data.get('sentense'),
            image_urls=image_urls,
            chapter=self.cleaned_data.get('chapter_id'),
            commentary=self.cleaned_data.get('commentary'),
            commentary_image_urls=commentary_image_urls,
        )
        self.create_answer(question, 1)
        self.create_answer(question, 2)
        self.create_answer(question, 3)
        self.create_answer(question, 4)
        return question


class QuestionUpdateForm(forms.Form):
    title = forms.CharField(required=True)
    sentense = forms.CharField(required=True)
    chapter_id = forms.CharField(required=False)
    image = forms.FileField(required=False)
    answer1_id = forms.CharField(required=True)
    answer1_title = forms.CharField(required=True)
    answer1_sentense = forms.CharField(required=True)
    answer2_id = forms.CharField(required=True)
    answer2_title = forms.CharField(required=True)
    answer2_sentense = forms.CharField(required=True)
    answer3_id = forms.CharField(required=True)
    answer3_title = forms.CharField(required=True)
    answer3_sentense = forms.CharField(required=True)
    answer4_id = forms.CharField(required=True)
    answer4_title = forms.CharField(required=True)
    answer4_sentense = forms.CharField(required=True)
    collect_answer_id = forms.CharField(required=True)
    commentary = forms.CharField(required=True)
    commentary_image = forms.FileField(required=False)

    def __init__(self, *args, **kwargs):
        self.context = kwargs.pop('context', {})
        super(QuestionUpdateForm, self).__init__(*args, **kwargs)
    
    def clean_chapter_id(self):
        chapter_id = self.cleaned_data.get('chapter_id')
        if chapter_id:
            try:
                chapter = models.Chapter.objects.get(chapter_id=chapter_id, workbook=self.context['workbook'])
            except models.Chapter.DoesNotExist:
                raise forms.ValidationError('このIDは存在しません')
            return chapter
    
    def clean_answer1_id(self):
        answer_id = self.cleaned_data.get('answer1_id')
        try:
            answer = models.Answer.objects.get(answer_id=answer_id)
        except models.Answer.DoesNotExist:
            raise forms.ValidationError('このIDは存在しません')
        return answer
    
    def clean_answer2_id(self):
        answer_id = self.cleaned_data.get('answer2_id')
        try:
            answer = models.Answer.objects.get(answer_id=answer_id)
        except models.Answer.DoesNotExist:
            raise forms.ValidationError('このIDは存在しません')
        return answer
    
    def clean_answer3_id(self):
        answer_id = self.cleaned_data.get('answer3_id')
        try:
            answer = models.Answer.objects.get(answer_id=answer_id)
        except models.Answer.DoesNotExist:
            raise forms.ValidationError('このIDは存在しません')
        return answer
    
    def clean_answer4_id(self):
        answer_id = self.cleaned_data.get('answer4_id')
        try:
            answer = models.Answer.objects.get(answer_id=answer_id)
        except models.Answer.DoesNotExist:
            raise forms.ValidationError('このIDは存在しません')
        return answer

    def update_answer(self, index):
        answer = self.cleaned_data.get('answer{}_id'.format(index))
        answer.title = self.cleaned_data.get('answer{}_title'.format(index))
        answer.sentense = self.cleaned_data.get('answer{}_sentense'.format(index))
        answer.is_true = self.cleaned_data.get('collect_answer_id') == str(answer.answer_id)
        answer.save()
    
    def upload(self, image_file):
        file_name = default_storage.save(image_file.name, image_file)
        return default_storage.url(file_name)

    def save(self):
        # 画像をアップロード
        image_file = self.cleaned_data['image']
        image_urls = []
        if image_file:
            image_url = self.upload(image_file)
            image_urls.append(image_url)
        
        commentary_image_file = self.cleaned_data['commentary_image']
        commentary_image_urls = []
        if image_file:
            commentary_image_url = self.upload(commentary_image_file)
            commentary_image_urls.append(commentary_image_url)

        question = self.context['question']
        question.title = self.cleaned_data.get('title')
        question.sentense = self.cleaned_data.get('sentense')
        question.image_urls = image_urls
        question.chapter = self.cleaned_data.get('chapter_id')
        question.commentary = self.cleaned_data.get('commentary')
        question.commentary_image_urls = commentary_image_urls
        question.save()

        # 回答選択肢を編集
        self.update_answer(1)
        self.update_answer(2)
        self.update_answer(3)
        self.update_answer(4)

        return question


class ChapterCreateForm(forms.Form):
    title = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        self.context = kwargs.pop('context', {})
        super(ChapterCreateForm, self).__init__(*args, **kwargs)

    def save(self):
        chapter = models.Chapter.objects.create(
            workbook=self.context['workbook'],
            title=self.cleaned_data.get('title'),
        )
        return chapter


class ChapterUpdateForm(forms.Form):
    title = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        self.context = kwargs.pop('context', {})
        super(ChapterUpdateForm, self).__init__(*args, **kwargs)

    def save(self):
        chapter = self.context['chapter']
        chapter.title = self.cleaned_data.get('title')
        chapter.save()
        return chapter


class WorkbookTrainingCreateForm(forms.Form):
    training_type = forms.ChoiceField(choices=models.Training.TrainingTypes.choices)

    def __init__(self, *args, **kwargs):
        self.context = kwargs.pop('context', {})
        super(WorkbookTrainingCreateForm, self).__init__(*args, **kwargs)

    def save(self):
        training = models.Training.objects.create(
            workbook=self.context['workbook'],
            user=self.context['request'].user,
            training_type=self.cleaned_data.get('training_type'),
        )
        return training


class WorkbookTrainingSelectChapterForm(forms.Form):
    chapter_ids = MultiValueField(forms.CharField(required=False), "chapter_ids")

    def __init__(self, *args, **kwargs):
        self.context = kwargs.pop('context', {})
        super(WorkbookTrainingSelectChapterForm, self).__init__(*args, **kwargs)
    
    def clean_chapter_ids(self):
        chapters = []
        chapter_ids = self.cleaned_data.get('chapter_ids')
        for chapter_id in chapter_ids:
            try:
                chapter = models.Chapter.objects.get(workbook=self.context['workbook'], chapter_id=chapter_id)
            except models.Chapter.DoesNotExist:
                raise forms.ValidationError('このIDは存在しません')
            chapters.append(chapter)
        return chapters

    
    def save(self):
        training_type = self.context.get('training_type')
        if not training_type:
            training_type = models.Training.TrainingTypes.SELECT_CHAPTER
        training = models.Training.objects.create(
            workbook=self.context['workbook'],
            user=self.context['request'].user,
            training_type=training_type,
        )
        # 関連するチャプターを保存
        for chapter in self.cleaned_data.get('chapter_ids'):
            models.TrainingChapter.objects.create(
                chapter=chapter,
                training=training,
            )
        return training


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


class WorkbookTrainingAnswerForm(forms.Form):
    not_confident = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        self.context = kwargs.pop('context', {})
        super(WorkbookTrainingAnswerForm, self).__init__(*args, **kwargs)

    def clean_not_confident(self):
        not_confident = self.cleaned_data['not_confident']
        if not_confident == True:
            return True
        else:
            return False

    def save(self):
        training_selection = self.context['training_selection']
        training_selection.confident = not self.cleaned_data['not_confident']
        training_selection.save()
        return training_selection