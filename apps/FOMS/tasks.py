from apps.FOMS.models import ArchviedFiles
from apps.FOMS.services.archived_file_processor import ArchiveFileProcessor
from apps.FOMS.services.excel_creator import ExcelCreator
from apps.FOMS.services.unpack_service import Unpacker
from apps.FOMS.utils import send_email, remove_files
from config.celery import app
import logging
import os


logger = logging.getLogger(__name__)


@app.task(time_limit=2500)
def archive_processor(batch_id, keyword):
    try:
        archived_files = ArchviedFiles.objects.filter(
            batch_id=batch_id
        )
        response_list = []
        final_file = 'Report.xlsx'
        for file in archived_files:
            unp = Unpacker(str(file.file))
            unp.process("extract_folder")
            files = [f for f in os.listdir(os.getcwd() + '/extract_folder')]
            for archived_file in files:
                fh = ArchiveFileProcessor(archived_file, keyword, str(file.file))
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

        remove_files('uploads')
        remove_files('extract_folder')
        remove_files('pdf_dir')
    except Exception as e:
        logger.info(f'Task has failed due to {e}')
        send_email(
            recipient='alexandr.jri.bystrov@yandex.ru',
            body=f'Не получилось обработать файлы из за ошибки /n {e}',
            subject='Отчёт по ФОМСам'
        )
