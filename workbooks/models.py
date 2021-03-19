import uuid

from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User

from lib.models import BaseModel
from . import managers



class Workbook(BaseModel, models.Model):
    workbook_id = models.UUIDField('問題集識別子', default=uuid.uuid4, unique=True, db_index=True)
    user = models.ForeignKey(User, db_index=True, on_delete=models.CASCADE)
    title = models.CharField('タイトル', max_length=250, db_index=True)
    description = models.TextField('詳細説明文', default=None, null=True, blank=True)

    objects = managers.WorkbookManager()

    class Meta:
        verbose_name = 'workbooks'
        verbose_name_plural = 'Workbook'

    def __str__(self):
        return str(self.title)


class Chapter(BaseModel, models.Model):
    chapter_id = models.CharField('章識別子', max_length=100, db_index=True)
    workbook = models.ForeignKey('workbooks.Workbook', db_index=True, on_delete=models.CASCADE)
    title = models.CharField('タイトル', max_length=250, db_index=True)
    description = models.TextField('詳細説明文', default=None, null=True, blank=True)

    objects = managers.ChapterManager()

    class Meta:
        verbose_name = 'chapters'
        verbose_name_plural = 'Chapter'
        unique_together = (
            ('chapter_id', 'workbook'),
        )

    def __str__(self):
        return str(self.title)


class Question(BaseModel, models.Model):
    question_id = models.CharField('問題識別子', max_length=100, unique=True, db_index=True)
    chapter = models.ForeignKey('workbooks.Chapter', db_index=True, on_delete=models.CASCADE, null=True, default=None, blank=True)
    workbook = models.ForeignKey('workbooks.Workbook', db_index=True, on_delete=models.CASCADE)
    title = models.CharField('タイトル', max_length=250, db_index=True)
    sentense = models.TextField('問題文')
    image_urls = ArrayField(models.URLField(), size=10, default=list)
    hint = models.TextField('問題ヒント文章', default=None, null=True, blank=True)
    commentary = models.TextField('正解解説文章', default=None, null=True, blank=True)
    commentary_image_urls = ArrayField(models.URLField(), size=10, default=list)

    objects = managers.QuestionManager()

    class Meta:
        verbose_name = 'questions'
        verbose_name_plural = 'Question'
        unique_together = (
            ('question_id', 'workbook'),
        )

    def __str__(self):
        return str(self.title)


class Answer(BaseModel, models.Model):
    answer_id = models.UUIDField('答えID', default=uuid.uuid4, unique=True, db_index=True)
    question = models.ForeignKey('workbooks.Question', db_index=True, on_delete=models.CASCADE)
    title = models.CharField('タイトル', max_length=250, db_index=True)
    sentense = models.TextField('問題文')
    is_true = models.BooleanField('正しい選択肢かどうか', default=False)

    objects = managers.AnswerManager()

    class Meta:
        verbose_name = 'answers'
        verbose_name_plural = 'Answer'

    def __str__(self):
        return str(self.title)


class Relationship(BaseModel, models.Model):
    relationship_id = models.UUIDField('類似ID', default=uuid.uuid4, unique=True, db_index=True)
    question1 = models.ForeignKey('workbooks.Question', db_index=True, on_delete=models.CASCADE, related_name="question1")
    question2 = models.ForeignKey('workbooks.Question', db_index=True, on_delete=models.CASCADE, related_name="question2")

    objects = managers.RelationshipManager()

    class Meta:
        verbose_name = 'relationships'
        verbose_name_plural = 'Relationship'


class Training(BaseModel, models.Model):
    training_id = models.UUIDField('イベントID', default=uuid.uuid4, unique=True, db_index=True)
    user = models.ForeignKey(User, db_index=True, on_delete=models.CASCADE)
    workbook = models.ForeignKey('workbooks.Workbook', db_index=True, on_delete=models.CASCADE)
    done = models.BooleanField('実施完了済みか', default=False)
    
    objects = managers.TrainingManager()

    class Meta:
        verbose_name = 'trainings'
        verbose_name_plural = 'Training'

    def __str__(self):
        return str(self.workbook.title)


class TrainingSelection(BaseModel, models.Model):
    training_selection_id = models.UUIDField('選択ID', default=uuid.uuid4, unique=True, db_index=True)
    training = models.ForeignKey('workbooks.Training', db_index=True, on_delete=models.CASCADE)
    question = models.ForeignKey('workbooks.Question', db_index=True, on_delete=models.CASCADE)
    answer = models.ForeignKey('workbooks.Answer', db_index=True, on_delete=models.CASCADE)
    correct = models.BooleanField('正解かどうか', default=False)
    duration = models.IntegerField('かかった時間[ms]')

    objects = managers.TrainingSelectionManager()

    class Meta:
        verbose_name = 'training_selections'
        verbose_name_plural = 'TrainingSelection'