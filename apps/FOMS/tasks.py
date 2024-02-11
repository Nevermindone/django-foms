from apps.FOMS.models import ArchviedFiles
from apps.FOMS.services.unpack_service import Unpacker
from config.celery import app
import logging
import os
os.environ["LC_ALL"] = "ru_RU.UTF-8"  # Установка локали на русский

logger = logging.getLogger(__name__)

@app.task(time_limit=2500)
def archive_processor(batch_id):
    archived_files = ArchviedFiles.objects.filter(
        batch_id=batch_id
    )
    for file in archived_files:
        unp = Unpacker(str(file.file))
        unp.process("extract_folder")

        # Archive(str(file.file)).extractall('extract_folder')

