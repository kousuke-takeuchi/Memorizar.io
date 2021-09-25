from django.core.files.storage import default_storage

from rest_framework import serializers


class MediaUploadSerializer(serializers.Serializer):
    file = serializers.FileField(required=True)

    def create(self, validated_data):
        file = validated_data['file']
        file_name = default_storage.save(file.name, file)
        return default_storage.url(file_name)