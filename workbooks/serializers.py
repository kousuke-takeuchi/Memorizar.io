from rest_framework import serializers

from . import models


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