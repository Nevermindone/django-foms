import os

from apps.FOMS.services.archive_processors.rar_processor import RarHandler
from apps.FOMS.services.archive_processors.zip_processor import ZipHandler


class Unpacker:
    def __init__(self, input_filepath):
        self.input_filepath = input_filepath
        self.processor_mapper = {
            '.rar': RarHandler,
            '.zip': ZipHandler
        }

    def _get_extension(self):
        file_name, file_extension = os.path.splitext(self.input_filepath)
        return file_extension

    def process(self, output_folder):
        extension = self._get_extension()
        processor = self.processor_mapper[extension]
        processor.process(self.input_filepath, output_folder)
