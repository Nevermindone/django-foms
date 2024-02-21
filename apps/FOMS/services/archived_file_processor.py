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

    def to_dict(self):
        return {k: v for k, v in asdict(self).items()}


class ArchiveFileProcessor:
    def __init__(self, file, keyword, archive_name=None):
        self.file = file
        self.keyword = keyword
        self.archive_name = archive_name
        self.handler_mapping = {
            '.xls': XlsFileHandler(file=self.file, keyword=self.keyword),
            '.xlsx': XlsFileHandler(file=self.file, keyword=self.keyword),
            '.doc': DocFileHandler(file=self.file, keyword=self.keyword),
            '.docx': DocFileHandler(file=self.file, keyword=self.keyword),
            '.pdf': PDFFileHandler(file=self.file, keyword=self.keyword),
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
                    error_message='Файл не верного типа, ожидал excel, doc или pdf'
                )]
            handler_response = handler.process_file()
            data_objects = []
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
                archive_name=self.archive_name,
                has_error=has_error,
                error_message=error
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
            error_message=error
        )
        return data
