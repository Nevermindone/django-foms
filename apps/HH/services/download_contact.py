import zipfile
from io import BytesIO
import time
from django.http import HttpResponse
from os.path import basename

from apps.HH.models import Urls


def download_zip(idq_list):
    paths = Urls.objects.filter(pk__in=idq_list).values_list('path', flat=True).all()
    s = BytesIO()
    s, zip_path = compress(list(paths), s)
    response = HttpResponse(s.getvalue(), content_type="application/x-zip-compressed")
    response['Content-Disposition'] = 'attachment; filename="%s"' % zip_path.split('/')[-1]
    return response


def compress(file_names, s):
    timestr = time.strftime("%m-%d-%Y %H:%M%p")
    zip_path_raw = "storage/contacts_%s.zip"
    zip_path = zip_path_raw % timestr
    zf = zipfile.ZipFile(s, mode="w")
    # try:
    for fpath in file_names:
        
        # fpath = 'storage/exmaple.docx'  # удалить строку когда будут реальные файлы
        zf.write(fpath,basename(fpath))

    zf.close()
    return s, zip_path
