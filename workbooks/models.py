import uuid

from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User

from lib.models import BaseModel
from . import managers
import workbooks


class Category(BaseModel, models.Model):
    category_id = models.UUIDField('カテゴリ識別子', default=uuid.uuid4, unique=True, db_index=True)
    user = models.ForeignKey(User, db_index=True, on_delete=models.CASCADE)
    title = models.CharField('タイトル', max_length=250, db_index=True)
    description = models.TextField('詳細説明文', default=None, null=True, blank=True)
    image_url = models.URLField('カテゴリー画像', default=None, null=True, blank=True)

    workbooks = models.ManyToManyField('workbooks.Workbook', through='workbooks.WorkbookCategory')

    objects = managers.CategoryManager()

    class Meta:
        verbose_name = 'categories'
        verbose_name_plural = 'Category'

    def __str__(self):
        return str(self.title)


class WorkbookCategory(BaseModel, models.Model):
    workbook = models.ForeignKey('workbooks.Workbook', db_index=True, on_delete=models.CASCADE)
    category = models.ForeignKey('workbooks.Category', db_index=True, on_delete=models.CASCADE)

    objects = managers.WorkbookCategoryManager()

    class Meta:
        verbose_name = 'workbook_categories'
        verbose_name_plural = 'WorkbookCategory'


class Workbook(BaseModel, models.Model):
    workbook_id = models.UUIDField('問題集識別子', default=uuid.uuid4, unique=True, db_index=True)
    user = models.ForeignKey(User, db_index=True, on_delete=models.CASCADE)
    title = models.CharField('タイトル', max_length=250, db_index=True)
    description = models.TextField('詳細説明文', default=None, null=True, blank=True)
    image_url = models.URLField('問題集画像', default=None, null=True, blank=True)
    publish = models.BooleanField('公開する', default=False)
    default_answer_count = models.IntegerField('回答選択肢の数', default=4)

    categories = models.ManyToManyField('workbooks.Category', through='workbooks.WorkbookCategory')
    
    objects = managers.WorkbookManager()

    class Meta:
        verbose_name = 'workbooks'
        verbose_name_plural = 'Workbook'

    def __str__(self):
        return str(self.title)


class Chapter(BaseModel, models.Model):
    chapter_id = models.CharField('章識別子', default=uuid.uuid4, max_length=100, db_index=True)
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


class QuestionGroup(BaseModel, models.Model):
    question_group_id = models.UUIDField('問題グループID', default=uuid.uuid4, unique=True, db_index=True)
    chapter = models.ForeignKey('workbooks.Chapter', db_index=True, on_delete=models.CASCADE, null=True, default=None, blank=True)
    workbook = models.ForeignKey('workbooks.Workbook', db_index=True, on_delete=models.CASCADE)
    title = models.CharField('タイトル', max_length=250, db_index=True)
    sentense = models.TextField('問題説明文')
    image_urls = ArrayField(models.URLField(), size=10, default=list)

    objects = managers.QuestionGroupManager()

    class Meta:
        verbose_name = 'question_groups'
        verbose_name_plural = 'QuestionGroup'

    def __str__(self):
        return str(self.title)


class Question(BaseModel, models.Model):
    question_id = models.CharField('問題識別子', default=uuid.uuid4, max_length=100, unique=True, db_index=True)
    chapter = models.ForeignKey('workbooks.Chapter', db_index=True, on_delete=models.CASCADE, null=True, default=None, blank=True)
    workbook = models.ForeignKey('workbooks.Workbook', db_index=True, on_delete=models.CASCADE)
    title = models.CharField('タイトル', max_length=250, db_index=True)
    sentense = models.TextField('問題文', default='', blank=True)
    image_urls = ArrayField(models.URLField(), size=10, default=list)
    hint = models.TextField('問題ヒント文章', default=None, null=True, blank=True)
    commentary = models.TextField('正解解説文章', default=None, null=True, blank=True)
    commentary_image_urls = ArrayField(models.URLField(), size=10, default=list)
    index = models.IntegerField('並び順', db_index=True, default=1)
    group = models.ForeignKey('workbooks.QuestionGroup', null=True, default=None, blank=True, db_index=True, on_delete=models.SET_NULL)

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
    index = models.IntegerField('並び順', db_index=True, default=1)

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
    class TrainingTypes(models.TextChoices):
        RANDOM = 'RAND', 'Random'
        SELECT_CHAPTER = 'CHAP', 'Select Chapter'
        REVIEW_MISTAKE = 'MIST', 'Review Mistake'
        ORDERED = 'ORDR', 'Ordered'

    training_id = models.UUIDField('イベントID', default=uuid.uuid4, unique=True, db_index=True)
    user = models.ForeignKey(User, db_index=True, on_delete=models.CASCADE)
    workbook = models.ForeignKey('workbooks.Workbook', db_index=True, on_delete=models.CASCADE)
    training_type = models.TextField('実施種別', max_length=4, choices=TrainingTypes.choices, default=TrainingTypes.RANDOM)
    done = models.BooleanField('実施完了済みか', default=False)

    chapters = models.ManyToManyField('workbooks.Chapter', through='workbooks.TrainingChapter')
    
    objects = managers.TrainingManager()

    class Meta:
        verbose_name = 'trainings'
        verbose_name_plural = 'Training'

    def __str__(self):
        return str(self.workbook.title)


class TrainingQuestion(BaseModel, models.Model):
    training_question_id = models.UUIDField('出題問題ID', default=uuid.uuid4, unique=True, db_index=True)
    training = models.ForeignKey('workbooks.Training', db_index=True, on_delete=models.CASCADE)
    question = models.ForeignKey('workbooks.Question', db_index=True, on_delete=models.CASCADE)
    index = models.IntegerField('並び順', db_index=True, default=1)
    
    objects = managers.TrainingQuestionManager()

    class Meta:
        verbose_name = 'training_questions'
        verbose_name_plural = 'TrainingQuestion'


class TrainingSelection(BaseModel, models.Model):
    training_selection_id = models.UUIDField('選択ID', default=uuid.uuid4, unique=True, db_index=True)
    training = models.ForeignKey('workbooks.Training', db_index=True, on_delete=models.CASCADE)
    question = models.ForeignKey('workbooks.Question', db_index=True, on_delete=models.CASCADE)
    answer = models.ForeignKey('workbooks.Answer', db_index=True, on_delete=models.CASCADE)
    correct = models.BooleanField('正解かどうか', default=False)
    confident = models.BooleanField('迷いがなかったかどうか', default=True)
    duration = models.IntegerField('かかった時間[ms]')

    objects = managers.TrainingSelectionManager()

    class Meta:
        verbose_name = 'training_selections'
        verbose_name_plural = 'TrainingSelection'


class TrainingChapter(BaseModel, models.Model):
    training = models.ForeignKey('workbooks.Training', db_index=True, on_delete=models.CASCADE)
    chapter = models.ForeignKey('workbooks.Chapter', db_index=True, on_delete=models.CASCADE)
    
    objects = managers.TrainingChapterManager()

    class Meta:
        verbose_name = 'training_chapters'
        verbose_name_plural = 'TrainingChapter'


class Registration(BaseModel, models.Model):
    user = models.ForeignKey(User, db_index=True, on_delete=models.CASCADE)
    workbook = models.ForeignKey('workbooks.Workbook', db_index=True, on_delete=models.CASCADE)

    objects = managers.RegistrationManager()

    class Meta:
        verbose_name = 'registrations'
        verbose_name_plural = 'Registration'