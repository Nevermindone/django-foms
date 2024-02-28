from logging import getLogger

from apps.FOMS.services.description_extractor import DescriptionProcessor
from apps.FOMS.services.handlers import XlsFileHandler, DocFileHandler, PDFFileHandler
from apps.FOMS.services.price_extractor import PriceProcessor
from apps.FOMS.utils import get_file_extension
from dataclasses import dataclass, asdict

logger = getLogger(__name__)


class ArchiveFileProcessorException(Exception):
    pass


@dataclass(frozen=True)
class OneRowOfDataKeyword:
    description: [str]
    price: [float]
    file: str
    page: [str]
    archive_name: [str]
    has_error: bool
    error_message: str
    main_data_object: bool
    error_data_object: bool

    def to_dict(self):
        return {k: v for k, v in asdict(self).items()}


class ArchiveFileProcessor:
    def __init__(self, file, keyword, archive_name=None, batch_id=None):
        self.file = file
        self.keyword = keyword
        self.archive_name = archive_name
        self.batch_id = batch_id
        self.handler_mapping = {
            '.xls': XlsFileHandler(file=self.file, keyword=self.keyword, current_batch=batch_id),
            '.xlsx': XlsFileHandler(file=self.file, keyword=self.keyword, current_batch=batch_id),
            # '.doc': DocFileHandler(file=self.file, keyword=self.keyword, current_batch=batch_id),
            # '.docx': DocFileHandler(file=self.file, keyword=self.keyword, current_batch=batch_id),
            '.pdf': PDFFileHandler(file=self.file, keyword=self.keyword, current_batch=batch_id),
        }
        self.dp = DescriptionProcessor(self.keyword)
        self.pp = PriceProcessor()

    def process(self, file) -> list[OneRowOfDataKeyword]:
        logger.info(f'File {file} has been started to process.')
        try:
            ext = get_file_extension(file)
            logger.info(f'File extension is {ext}')
            handler = self.handler_mapping.get(ext)

            if not handler:
                return [OneRowOfDataKeyword(
                    description=None,
                    price=None,
                    file=file,
                    page=None,
                    archive_name=self.archive_name,
                    has_error=True,
                    error_message='Обработчик для данного расширения файла не предусмотрен, '
                                  'ожидались excel, doc или pdf',
                    main_data_object=False,
                    error_data_object=False,
                )]
            handler_response = handler.process_file()
            data_objects = []
            if not handler_response:
                return [OneRowOfDataKeyword(
                    description=None,
                    price=None,
                    file=file,
                    page=1,
                    archive_name=self.archive_name,
                    has_error=False,
                    error_message='Не найдено совпадений',
                    main_data_object=False,
                    error_data_object=False,
                )]
            for page_from_handler in handler_response:
                data_object = self._extract_info(page_from_handler)
                data_objects.append(data_object)
            return data_objects
        except ArchiveFileProcessorException as e:
            description = None
            price = None
            error = f'{e}'
            has_error = True
            data = OneRowOfDataKeyword(
                description=description,
                price=price,
                file=file,
                page=None,
                archive_name=self.archive_name,
                has_error=has_error,
                error_message=error,
                main_data_object=False,
                error_data_object=True,
            )
            return [data]

    def _extract_info(self, page_from_handler):
        error = ''
        has_error = False
        file = page_from_handler[-2]
        page = page_from_handler[-1]
        description = self.dp.find_and_process_description(page_from_handler)
        pp = PriceProcessor()
        price = pp.find_price(page_from_handler)

        data = OneRowOfDataKeyword(
            description=description,
            price=price,
            file=file,
            page=page,
            archive_name=self.archive_name,
            has_error=has_error,
            error_message=error,
            main_data_object=True,
            error_data_object=False,
        )
        return data
