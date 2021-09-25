from rest_framework.views import APIView

from lib.responses import SuccessResponse, ErrorResponse
from . import serializers



class MediaUploadView(APIView):
    def post(self, request):
        serializer = serializers.MediaUploadSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid(raise_exception=False):
            return ErrorResponse(serializer.errors)
        file_url = serializer.save()
        return SuccessResponse({'file_url': file_url})