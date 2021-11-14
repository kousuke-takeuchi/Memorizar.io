import io
import time
import uuid
import tempfile

from PIL import Image

from django.core.files.base import ContentFile
from django.utils import timezone
from django.core.files.storage import default_storage

from rest_framework import serializers

from . import models


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField(required=True)
    width = serializers.IntegerField(required=False)
    height = serializers.IntegerField(required=False)
    top = serializers.IntegerField(required=False)
    left = serializers.IntegerField(required=False)

    def save(self):
        inmemory_file = self.validated_data['file']
        filename = str(uuid.uuid4()) + '.png'
        file_path = 'remote_files/' + filename

        width = self.validated_data['width']
        height = self.validated_data['height']
        top = self.validated_data['top']
        left = self.validated_data['left']
        image = Image.open(inmemory_file)
        image = image.crop((left, top, left+width, top+height))

        imageBuffer = io.BytesIO()
        image.save(imageBuffer, 'png')
        filename = default_storage.save(file_path, ContentFile(imageBuffer.getvalue()))
        image_url = default_storage.url(filename)
        image_url = image_url.split('?')[0]
        return image_url


class WorkbookSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Workbook
        read_only_fields = ('workbook_id',)
        write_only_fields = ()
        fields = read_only_fields + write_only_fields + (
            'title', 'description'
        )
        extra_kwargs = dict([(field, {'write_only': True, 'required': True}) for field in write_only_fields])
  
    def create(self, validated_data):
        workbook = models.Workbook.objects.create(
            title=validated_data['title'],
            description=validated_data['description'],
            user=self.context['request'].user,
        )
        return workbook
    
    def update(self, workbook, validated_data):
        workbook.title = validated_data['title']
        workbook.description = validated_data['description']
        workbook.save()
        return workbook


class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Chapter
        read_only_fields = ('chapter_id',)
        write_only_fields = ()
        fields = read_only_fields + write_only_fields + (
            'title', 'description'
        )
        extra_kwargs = dict([(field, {'write_only': True, 'required': True}) for field in write_only_fields])
    
    def validate_chapter_id(self, chapter_id):
        try:
            chapter = models.Chapter.objects.get(chapter_id=chapter_id)
        except models.Chapter.DoesNotExist:
            raise serializers.ValidationError('このIDは存在しません')
        return chapter
    
    def create(self, validated_data):
        chapter = models.Question.objects.create(
            title=validated_data['title'],
            description=validated_data['description'],
            workbook=self.context['workbook'],
        )
        return chapter
    
    def update(self, chapter, validated_data):
        chapter.title = validated_data['title']
        chapter.sentense = validated_data['sentense']
        chapter.save()
        return chapter


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        read_only_fields = ('answer_id',)
        write_only_fields = ()
        fields = read_only_fields + write_only_fields + (
            'sentense', 'index',
        )
        extra_kwargs = dict([(field, {'write_only': True, 'required': True}) for field in write_only_fields])


class QuestionSerializer(serializers.ModelSerializer):
    chapter = ChapterSerializer(read_only=True)
    answers = AnswerSerializer(source="answer_set.all", many=True)
    chapter_id = serializers.CharField(write_only=True)
    correct_index = serializers.IntegerField(write_only=True)

    class Meta:
        model = models.Question
        read_only_fields = ('question_id', 'chapter',)
        write_only_fields = ('chapter_id', 'correct_index',)
        fields = read_only_fields + write_only_fields + (
            'title', 'sentense', 'image_urls', 'commentary', 'commentary_image_urls', 'answers',
        )
        extra_kwargs = dict([(field, {'write_only': True, 'required': True}) for field in write_only_fields])
    
    def validate_chapter_id(self, chapter_id):
        try:
            chapter = models.Chapter.objects.get(chapter_id=chapter_id)
        except models.Chapter.DoesNotExist:
            raise serializers.ValidationError('このIDは存在しません')
        return chapter
  
    def create(self, validated_data):
        question = models.Question.objects.create(
            title=validated_data['title'],
            sentense=validated_data['sentense'],
            chapter=validated_data['chapter_id'],
            image_urls=validated_data.get('image_urls', []),
            commentary=validated_data['commentary'],
            commentary_image_urls=validated_data.get('commentary_image_urls', []),
            workbook=self.context['workbook'],
        )
        for answer_data in validated_data['answer_set']['all']:
            models.Answer.objects.create(
                question=question,
                title=answer_data['index'],
                sentense=answer_data['sentense'],
                index=answer_data['index'],
                is_true=answer_data['index'] == validated_data['correct_index']
            )
        return question
    

    def update(self, question, validated_data):
        question.title = validated_data.get('title')
        question.sentense = validated_data.get('sentense')
        question.index = validated_data.get('index')
        question.commentary = validated_data.get('commentary')
        question.commentary_image_urls = validated_data.get('commentary_image_urls')
        question.save()
        return question


class TrainingSerializer(serializers.ModelSerializer):
    chapter_ids = ChapterSerializer(many=True, write_only=True)
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = models.Training
        read_only_fields = ('training_id', 'questions')
        write_only_fields = ('training_type', 'chapter_ids',)
        fields = read_only_fields + write_only_fields + ()
        extra_kwargs = dict([(field, {'write_only': True, 'required': True}) for field in write_only_fields])
  
    def create(self, validated_data):
        training = models.Training.objects.create(
            user=self.context['request'].user,
            workbook=self.context['workbook'],
            training_type=validated_data['training_type'],
        )
        for chapter in validated_data['chapter']:
            training.chapters.add(chapter)
        training.save()
        # 問題を10問まで選択して追加する
        return training


class TrainingQuestionSerializer(serializers.ModelSerializer):
    question = QuestionSerializer()
    class Meta:
        model = models.TrainingQuestion
        read_only_fields = ('index', 'question')
        write_only_fields = ()
        fields = read_only_fields + write_only_fields + ()
        extra_kwargs = dict([(field, {'write_only': True, 'required': True}) for field in write_only_fields])


class TrainingSelectionSerializer(serializers.ModelSerializer):
    selected_id = serializers.CharField(required=True, write_only=True)
    question_id = serializers.CharField(required=True, write_only=True)
    started_at = serializers.FloatField(required=True, write_only=True)

    training = TrainingSerializer(read_only=True)
    question = QuestionSerializer(read_only=True)
    answer = AnswerSerializer(read_only=True)

    class Meta:
        model = models.TrainingSelection
        read_only_fields = (
            'training_selection_id', 'training', 'question',
            'answer', 'correct', 'duration',
        )
        write_only_fields = ('selected_id', 'question_id', 'started_at',)
        fields = read_only_fields + write_only_fields + ()
        extra_kwargs = dict([(field, {'write_only': True, 'required': True}) for field in write_only_fields])
    
    def validate_selected_id(self, selected_id):
        try:
            selected_answer = models.Answer.objects.get(answer_id=selected_id)
        except models.Answer.DoesNotExist:
            raise serializers.ValidationError('このIDは存在しません')
        return selected_answer
    
    def validate_question_id(self, question_id):
        try:
            question = models.Question.objects.get(question_id=question_id)
        except models.Question.DoesNotExist:
            raise serializers.ValidationError('このIDは存在しません')
        return question

    def validate_started_at(self, started_at):
        current_time = int(timezone.now().timestamp())
        if started_at >= current_time:
            raise serializers.ValidationError('過去のUnixtimeを指定してください')
        return current_time - started_at

    def create(self, validated_data):
        question = validated_data['question_id']
        selected_answer = validated_data['selected_id']

        # 同じ実施内で同じ問題を解いた場合は、過去の選択を削除する
        duplicated_selections = models.TrainingSelection.objects.filter(
            training=self.context['training'],
            question=question,
        )
        duplicated_selections.delete()

        training_selection = models.TrainingSelection.objects.create(
            training=self.context['training'],
            question=question,
            answer=selected_answer,
            correct=selected_answer.is_true,
            duration=time.time() - validated_data['started_at'],
        )

        return training_selection


class QuestionGroupSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)
    chapter_id = serializers.CharField(write_only=True)

    class Meta:
        model = models.QuestionGroup
        read_only_fields = ('chapter',)
        write_only_fields = ('chapter_id',)
        fields = read_only_fields + write_only_fields + (
            'image_urls', 'title', 'sentense', 'questions',
        )
        extra_kwargs = dict([(field, {'write_only': True, 'required': True}) for field in write_only_fields])


    def create(self, validated_data):
        question_group = models.QuestionGroup.objects.create(
            workbook=self.context['workbook'],
            title=validated_data['title'],
            sentense=validated_data['sentense'],
            image_urls=validated_data.get('image_urls', []),
        )

        for question_data in validated_data.get('questions', []):
            question = models.Question.objects.create(
                title=question_data['title'],
                sentense=question_data['sentense'],
                chapter=question_data['chapter_id'],
                image_urls=question_data.get('image_urls', []),
                commentary=question_data['commentary'],
                commentary_image_urls=question_data.get('commentary_image_urls', []),
                workbook=self.context['workbook'],
                group=question_group,
            )
            for answer_data in question_data['answer_set']['all']:
                models.Answer.objects.create(
                    question=question,
                    title=answer_data['index'],
                    sentense=answer_data['sentense'],
                    index=answer_data['index'],
                    is_true=answer_data['index'] == question_data['correct_index']
                )
        return question_group