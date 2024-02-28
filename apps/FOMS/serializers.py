import os
from rest_framework import serializers

from apps.FOMS.utils import get_file_extension


class FilesSerializer(serializers.Serializer):
    file = serializers.ListField()
    filename = serializers.ListField()

    def validate_file(self, files):
        for file in files:
            if file == '':
                raise serializers.ValidationError("file field should not be empty.")
            ext = get_file_extension(str(file))
            allowed_extensions = ['.zip', '.rar', '.pdf', '.xls', '.doc', '.docx']
            if not ext.lower() in allowed_extensions:
                raise serializers.ValidationError("Only ZIP or RAR files are allowed.")
        return files


# class FileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = File
#         fields = ('name', 'file')
#
#     def validate_file(self, file):
#         allowed_extensions = ['.zip', '.rar']  # Add your desired file extensions here
#         file_extension = file.name.split('.')[-1].lower()
#
#         if file_extension not in allowed_extensions:
#             raise serializers.ValidationError(
#                 "Invalid file extension. Only {} files are allowed.".format(", ".join(allowed_extensions)))
#
#         return file
