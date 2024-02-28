from apps.FOMS.models import ArchviedFiles
from apps.FOMS.services.archived_file_processor import ArchiveFileProcessor
from apps.FOMS.services.excel_creator import ExcelCreator
from apps.FOMS.services.unpack_service import Unpacker
from apps.FOMS.utils import send_email, remove_files, get_file_extension
from config.celery import app
import logging
import os
import shutil


logger = logging.getLogger(__name__)


@app.task(time_limit=2500)
def archive_processor(batch_id, keyword):
    archived_files = ArchviedFiles.objects.filter(
        batch_id=batch_id
    )
    # creating folder structure
    current_extract_folder = f"extract_folder/{batch_id}"
    current_pdf_folder = f"pdf_dir/{batch_id}"
    current_uploads_folder = f"uploads/{batch_id}"
    os.mkdir(current_extract_folder, 0o754)
    os.mkdir(current_pdf_folder, 0o754)
    try:
        # start processing
        response_list = []
        final_file = 'Report.xlsx'
        for file in archived_files:
            ext = get_file_extension(str(file.file))
            if ext not in ['.rar', '.zip']:
                shutil.copy(str(file.file), current_extract_folder)
            else:
                unp = Unpacker(str(file.file))
                unp.process(current_extract_folder)
            files = [f for f in os.listdir(os.getcwd() + '/' + current_extract_folder)]
            for archived_file in files:
                fh = ArchiveFileProcessor(archived_file, keyword, str(file.file), batch_id)
                keyword_response = fh.process(archived_file)
                response_list.extend(keyword_response)
        excel_maker = ExcelCreator(response_list)
        excel_maker.make_excel(final_file)
        send_email(
            recipient='alexandr.jri.bystrov@yandex.ru',
            attachment_path=final_file,
            body='сформированный отчет',
            subject='Отчёт по ФОМСам'
        )

        remove_files(current_extract_folder)
        remove_files(current_pdf_folder)
        remove_files(current_uploads_folder)
    except Exception as e:
        logger.info(f'Task has failed due to {e}')
        send_email(
            recipient='alexandr.jri.bystrov@yandex.ru',
            body=f'Не получилось обработать файлы из за ошибки {e}',
            subject='Отчёт по ФОМСам'
        )
        remove_files(current_extract_folder)
        remove_files(current_pdf_folder)
        remove_files(current_uploads_folder)

