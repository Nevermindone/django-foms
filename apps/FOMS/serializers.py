import os

from rest_framework import serializers

from apps.FOMS.models import File


# class FileSerializer(serializers.Serializer):
#     file = serializers.FileField()
#
#     def validate_file(self, value):
#         ext = os.path.splitext(value.name)[1]  # получение расширения файла
#         allowed_extensions = ['.zip', '.rar']
#         if not ext.lower() in allowed_extensions:
#             raise serializers.ValidationError("Only ZIP or RAR files are allowed.")
#         return value


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('name', 'file')

    def validate_file(self, file):
        allowed_extensions = ['.zip', '.rar']  # Add your desired file extensions here
        file_extension = file.name.split('.')[-1].lower()

        if file_extension not in allowed_extensions:
            raise serializers.ValidationError(
                "Invalid file extension. Only {} files are allowed.".format(", ".join(allowed_extensions)))

        return file
