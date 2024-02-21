from django.shortcuts import render
from rest_framework.views import APIView

from apps.FOMS.models import ArchviedFiles, BatchUpload
from apps.FOMS.serializers import FilesSerializer
from apps.FOMS.tasks import archive_processor
from config.celery import app


class UploadCreateView(APIView):

    serializer_class = FilesSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        files_and_names_list = list(set(zip(data['file'], data['filename'])))
        bu = BatchUpload(
            archives_count=len(files_and_names_list)
        )
        bu.save()
        for file_object in files_and_names_list:
            af = ArchviedFiles(
                name=file_object[1],
                file=file_object[0],
                batch=bu
            )
            af.save()
        app.send_task(
            "apps.FOMS.tasks.archive_processor",
            [bu.pk, 'менинг'],
        )
        # archive_processor(bu.pk, 'менинг')
        return render(request, 'success.html')


def upload(request):
    return render(request, 'upload.html')
