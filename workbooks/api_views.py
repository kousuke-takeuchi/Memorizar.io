from django.shortcuts import get_object_or_404

from rest_framework.views import APIView

from lib import mixins
from lib.responses import SuccessResponse, ErrorResponse
from . import models, serializers


class FileUploadView(mixins.MemorizarBaseMixin, APIView):
    def post(self, request):
        serializer = serializers.FileUploadSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid(raise_exception=False):
            return ErrorResponse(serializer.errors)
        url = serializer.save()
        return SuccessResponse({'url': url})


class WorkbookListView(mixins.MemorizarBaseMixin, APIView):
    def get_querysets(self):
        workbooks = models.Workbook.objects.filter(user=self.request.user)
        return workbooks
        
    def get(self, request):
        querysets = self.get_querysets()
        serializer = serializers.WorkbookSerializer(querysets, many=True, context={'request': request})
        return SuccessResponse({'workbooks': serializer.data})
    
    def post(self, request):
        serializer = serializers.WorkbookSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid(raise_exception=False):
            return ErrorResponse(serializer.errors)
        serializer.save()
        return SuccessResponse({})


class WorkbookDetailView(mixins.MemorizarBaseMixin, APIView):
    def get_querysets(self, workbook_id):
        workbook = get_object_or_404(models.Workbook, workbook_id=workbook_id)
        return workbook
        
    def get(self, request, workbook_id):
        querysets = self.get_querysets(workbook_id)
        serializer = serializers.WorkbookSerializer(querysets, context={'request': request})
        return SuccessResponse({'workbook': serializer.data})


class ChapterListView(mixins.MemorizarBaseMixin, APIView):
    def get_querysets(self, workbook_id):
        chapters = models.Chapter.objects.filter(user=self.request.user, workbook__workbook_id=workbook_id)
        return chapters
        
    def get(self, request, workbook_id):
        querysets = self.get_querysets(workbook_id)
        serializer = serializers.ChapterSerializer(querysets, many=True, context={'request': request})
        return SuccessResponse({'chapters': serializer.data})
    
    def post(self, request, workbook_id):
        serializer = serializers.ChapterSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid(raise_exception=False):
            return ErrorResponse(serializer.errors)
        serializer.save()
        return SuccessResponse({})


class ChapterDetailView(mixins.MemorizarBaseMixin, APIView):
    def get_querysets(self, workbook_id, chapter_id):
        chapter = get_object_or_404(models.Chapter, user=self.request.user, workbook__workbook_id=workbook_id, chapter_id=chapter_id)
        return chapter
        
    def get(self, request, workbook_id, chapter_id):
        querysets = self.get_querysets(workbook_id, chapter_id)
        serializer = serializers.ChapterSerializer(querysets, context={'request': request})
        return SuccessResponse({'question': serializer.data})
    
    def post(self, request, workbook_id, chapter_id):
        question = self.get_querysets(workbook_id, chapter_id)
        serializer = serializers.ChapterSerializer(question, data=request.data, context={'request': request})
        if not serializer.is_valid(raise_exception=False):
            return ErrorResponse(serializer.errors)
        serializer.save()
        return SuccessResponse({})


class QuestionListView(mixins.MemorizarBaseMixin, APIView):
    def get_querysets(self, workbook_id):
        questions = models.Question.objects.filter(user=self.request.user, workbook__workbook_id=workbook_id)
        return questions

    def get_workbook(self, workbook_id):
        workbook = get_object_or_404(models.Workbook, workbook_id=workbook_id)
        return workbook
        
    def get(self, request, workbook_id):
        querysets = self.get_querysets(workbook_id)
        serializer = serializers.QuestionSerializer(querysets, many=True, context={'request': request})
        return SuccessResponse({'questions': serializer.data})
    
    def post(self, request, workbook_id):
        workbook = self.get_workbook(workbook_id)
        serializer = serializers.QuestionSerializer(data=request.data, context={'request': request, 'workbook': workbook})
        if not serializer.is_valid(raise_exception=False):
            return ErrorResponse(serializer.errors)
        serializer.save()
        return SuccessResponse({})


class QuestionDetailView(mixins.MemorizarBaseMixin, APIView):
    def get_querysets(self, workbook_id, question_id):
        question = get_object_or_404(models.Question, workbook__user=self.request.user, workbook__workbook_id=workbook_id, question_id=question_id)
        return question
        
    def get(self, request, workbook_id, question_id):
        querysets = self.get_querysets(workbook_id, question_id)
        serializer = serializers.QuestionSerializer(querysets, context={'request': request})
        return SuccessResponse({'question': serializer.data})
    
    def post(self, request, workbook_id, question_id):
        question = self.get_querysets(workbook_id, question_id)
        serializer = serializers.QuestionSerializer(question, data=request.data, context={'request': request})
        if not serializer.is_valid(raise_exception=False):
            return ErrorResponse(serializer.errors)
        serializer.save()
        return SuccessResponse({})


class QuestionDeleteView(mixins.MemorizarBaseMixin, APIView):
    def get_querysets(self, workbook_id, question_id):
        question = get_object_or_404(models.Question, question_id=question_id, workbook__workbook_id=workbook_id)
        return question

    def post(self, request, workbook_id, question_id):
        question = self.get_querysets(workbook_id, question_id)
        question.delete()
        return SuccessResponse({})


class QuestionGroupListView(mixins.MemorizarBaseMixin, APIView):
    def get_querysets(self, workbook_id):
        questionGroup = models.QuestionGroup.objects.filter(user=self.request.user, workbook__workbook_id=workbook_id)
        return questionGroup

    def get_workbook(self, workbook_id):
        workbook = get_object_or_404(models.Workbook, workbook_id=workbook_id)
        return workbook
        
    def get(self, request, workbook_id):
        querysets = self.get_querysets(workbook_id)
        serializer = serializers.QuestionGroupSerializer(querysets, many=True, context={'request': request})
        return SuccessResponse({'question_groups': serializer.data})
    
    def post(self, request, workbook_id):
        print(request.data)
        workbook = self.get_workbook(workbook_id)
        serializer = serializers.QuestionGroupSerializer(data=request.data, context={'request': request, 'workbook': workbook})
        if not serializer.is_valid(raise_exception=False):
            return ErrorResponse(serializer.errors)
        serializer.save()
        return SuccessResponse({})


class TrainingListView(mixins.MemorizarBaseMixin, APIView):
    def get_querysets(self, workbook_id):
        workbook = get_object_or_404(models.Workbook, user=self.request.user, workbook_id=workbook_id)
        return workbook

    def post(self, request, workbook_id):
        workbook = self.get_querysets(workbook_id)
        serializer = serializers.TrainingSerializer(data=request.data, context={'request': request, 'workbook': workbook})
        if not serializer.is_valid(raise_exception=False):
            return ErrorResponse(serializer.errors)
        serializer.save()
        return SuccessResponse({})


class TrainingQuestionListView(mixins.MemorizarBaseMixin, APIView):
    def get_querysets(self, workbook_id, training_id):
        training = get_object_or_404(models.Training, workbook__workbook_id=workbook_id, training_id=training_id)
        questions = models.TrainingQuestion.objects.filter(training=training)
        return questions
        
    def get(self, request, workbook_id, training_id):
        querysets = self.get_querysets(workbook_id, training_id)
        serializer = serializers.TrainingQuestionSerializer(querysets, many=True, context={'request': request})
        return SuccessResponse({'training_questions': serializer.data})


class TrainingSelectionListView(mixins.MemorizarBaseMixin, APIView):
    def get_querysets(self, workbook_id, training_id):
        training = get_object_or_404(models.Training, workbook__workbook_id=workbook_id, training_id=training_id)
        return training

    def post(self, request, workbook_id, training_id):
        training = self.get_querysets(workbook_id, training_id)
        serializer = serializers.TrainingSelectionSerializer(data=request.data, context={'request': request, 'training': training})
        if not serializer.is_valid(raise_exception=False):
            return ErrorResponse(serializer.errors)
        selection = serializer.save()
        serializer = serializers.TrainingSelectionSerializer(selection, context={'request': request, 'training': training})
        return SuccessResponse({'selection': serializer.data})