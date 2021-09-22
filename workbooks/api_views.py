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


class WorkbookDetailView(mixins.MemorizarBaseMixin, APIView):
    def get_querysets(self, workbook_id):
        workbook = get_object_or_404(models.Workbook, workbook_id=workbook_id)
        return workbook
        
    def get(self, request, workbook_id):
        querysets = self.get_querysets(workbook_id)
        serializer = serializers.WorkbookSerializer(querysets, context={'request': request})
        return SuccessResponse({'workbook': serializer.data})