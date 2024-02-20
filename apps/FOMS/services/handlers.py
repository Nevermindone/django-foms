import os
from logging import getLogger

import pandas as pd
from abc import ABC, abstractmethod
import camelot
import PyPDF2
from apps.FOMS.utils import export_to_pdf

logger = getLogger(__name__)


class FileHandler(ABC):
    @abstractmethod
    def process_file(self) -> list:
        raise NotImplementedError


class BaseHandler(FileHandler):
    def __init__(self, file, keyword):
        self.file = file
        self.keyword = keyword

    def process_file(self):
        return None

    def parse_pdf(self, pdf_filepath):
        reader = PyPDF2.PdfReader(open(pdf_filepath, mode='rb'))
        page_number = len(reader.pages)
        pages = str(list(range(1, page_number + 1)))[1:-1]
        tables = camelot.read_pdf(pdf_filepath, pages=pages)
        results_list = []
        for count, table in enumerate(tables):
            df = table.df
            df['filename'] = pdf_filepath
            df['page'] = count + 1
            result = df[df.map(lambda x: self.keyword in str(x).lower()).any(axis=1)]
            results_list.append(result)
        results_list = [result.values.flatten().tolist() for result in results_list if len(result) > 0]
        return results_list


class XlsFileHandler(BaseHandler):
    def process_file(self):
        logger.info(f'XlsFileHandler {self.file} has been started to process')
        results = []
        sheet_to_df_map = pd.read_excel(f'extract_folder/{self.file}', sheet_name=None)
        keys = list(sheet_to_df_map.keys())
        for key in keys:
            df = sheet_to_df_map[key]
            df['filename'] = self.file
            df['page'] = key
            keywords_instances = df[df.map(lambda x: self.keyword in str(x).lower()).any(axis=1)]
            results.append(keywords_instances)
        results_list = [result.values.flatten().tolist() for result in results if len(result) > 0]
        logger.info(f'File {self.file} has been finished to process. Data objects are:')
        logger.info(results_list)
        return results_list


class DocFileHandler(BaseHandler):
    def process_file(self):
        logger.info(f'DocFileHandler {self.file} has been started to process')

        initial_filepath = f'extract_folder/{self.file}'
        pdf_filepath = f'pdf_dir/{os.path.splitext(self.file)[0]}.pdf'

        export_to_pdf(initial_filepath, 'pdf_dir')
        results_list = self.parse_pdf(pdf_filepath)
        logger.info(f'File {self.file} has been finished to process. Data objects are:')
        logger.info(results_list)
        return results_list


class PDFFileHandler(BaseHandler):
    def process_file(self):
        logger.info(f'PDFFileHandler {self.file} has been started to process')
        initial_filepath = f'extract_folder/{self.file}'
        results_list = self.parse_pdf(initial_filepath)
        logger.info(f'File {self.file} has been finished to process. Data objects are:')
        logger.info(results_list)
        return results_list
