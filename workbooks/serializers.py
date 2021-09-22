from rest_framework import serializers

from . import models


class WorkbookSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Workbook
        read_only_fields = ('workbook_id',)
        fields = read_only_fields + ('title', 'description',)