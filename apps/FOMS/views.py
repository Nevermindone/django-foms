import zipfile
import os
from django.conf import settings
from django.shortcuts import render

from apps.FOMS.forms import UploadForm

from django.views.generic import CreateView

from apps.FOMS.serializers import FileSerializer


class UploadCreateView(CreateView):

    def get(self, request, *args, **kwargs):
        return render(request, 'upload.html')

    def post(self, request, *args, **kwargs):
        print(request.FILES)
        # files = request.FILES.getlist("file")
        # print({"files": files})
        # serializer = FileSerializer(data=files, many=True)
        # serializer.is_valid(raise_exception=True)
        # data = serializer.validated_data
        # print(data)
        return render(request, 'success.html')


def upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            zip_file = request.FILES['file']
            with zipfile.ZipFile(zip_file, 'r') as archive:
                for file in archive.namelist():
                    archive.extract(file, os.path.join(settings.MEDIA_ROOT, 'uploads/'))
            return render(request, 'success.html')
    else:
        form = UploadForm()
    return render(request, 'upload.html', {'form': form})
