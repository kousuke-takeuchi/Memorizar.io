from rest_framework import serializers

from . import models
import workbooks


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
            'title', 'sentense', 'index',
        )
        extra_kwargs = dict([(field, {'write_only': True, 'required': True}) for field in write_only_fields])


class QuestionSerializer(serializers.ModelSerializer):
    chapter = ChapterSerializer()
    answers = AnswerSerializer(source="answer_set.all", many=True)

    class Meta:
        model = models.Question
        read_only_fields = ('question_id', 'chapter')
        write_only_fields = ('chapter_id',)
        fields = read_only_fields + write_only_fields + (
            'image_urls', 'title', 'sentense',
            'commentary', 'commentary_image_urls', 'index',
            'answers',
        )
        extra_kwargs = dict([(field, {'write_only': True, 'required': True}) for field in write_only_fields])
  
    def create(self, validated_data):
        question = models.Question.objects.create(
            title=validated_data['title'],
            sentense=validated_data['sentense'],
            index=validated_data['index'],
            commentary=validated_data['commentary'],
            commentary_image_urls=validated_data['commentary_image_urls'],
            workbook=self.context['workbook'],
        )
        for answer_data in validated_data['answers']:
            models.Answer.objects.create(
                title=answer_data['title'],
                sentense=answer_data['sentense'],
                index=answer_data['index'],    
            )
        return question
    

    def update(self, question, validated_data):
        question.title = validated_data['title']
        question.sentense = validated_data['sentense']
        question.index = validated_data['index']
        question.commentary = validated_data['commentary']
        question.commentary_image_urls = validated_data['commentary_image_urls']
        question.save()
        return question


class TrainingSerializer(serializers.ModelSerializer):
    chapters = ChapterSerializer(many=True)
    questions = QuestionSerializer(many=True)

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