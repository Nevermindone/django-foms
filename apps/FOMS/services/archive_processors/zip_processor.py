import zipfile


class ZipHandler:
    @staticmethod
    def process(input_file, output):
        with zipfile.ZipFile(input_file, 'r') as zip_ref:
            zip_ref.extractall(output)
