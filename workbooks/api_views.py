from django.shortcuts import get_object_or_404

from rest_framework.views import APIView

from lib import mixins
from lib.responses import SuccessResponse, ErrorResponse
from . import models, serializers



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


class QuestionListView(mixins.MemorizarBaseMixin, APIView):
    def get_querysets(self):
        questions = models.Question.objects.filter(user=self.request.user)
        return questions
        
    def get(self, request):
        querysets = self.get_querysets()
        serializer = serializers.QuestionSerializer(querysets, many=True, context={'request': request})
        return SuccessResponse({'workbooks': serializer.data})
    
    def post(self, request):
        serializer = serializers.QuestionSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid(raise_exception=False):
            return ErrorResponse(serializer.errors)
        serializer.save()
        return SuccessResponse({})


class QuestionDetailView(mixins.MemorizarBaseMixin, APIView):
    def get_querysets(self, question_id):
        question = get_object_or_404(models.Question, user=self.request.user, question_id=question_id)
        return question
        
    def get(self, request, question_id):
        querysets = self.get_querysets(question_id)
        serializer = serializers.QuestionSerializer(querysets, context={'request': request})
        return SuccessResponse({'workbooks': serializer.data})
    
    def post(self, request, question_id):
        question = self.get_querysets(question_id)
        serializer = serializers.QuestionSerializer(question, data=request.data, context={'request': request})
        if not serializer.is_valid(raise_exception=False):
            return ErrorResponse(serializer.errors)
        serializer.save()
        return SuccessResponse({})