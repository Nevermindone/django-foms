import os
import shutil
import zipfile


class ZipHandler:
    @staticmethod
    def process(input_file, output):
        # with zipfile.ZipFile(input_file, 'r') as zip_ref:
        #     zip_ref.extractall(output)

        with zipfile.ZipFile(input_file) as zip_file:
            for member in zip_file.namelist():
                filename = os.path.basename(member)
                # skip directories
                if not filename:
                    continue

                # copy file (taken from zipfile's extract)
                source = zip_file.open(member)
                print(filename)
                try:
                    target_name = os.path.join(output, filename.encode('cp437').decode('cp866'))
                except:
                    target_name = os.path.join(output, filename)
                target = open(target_name, "wb")
                with source, target:
                    shutil.copyfileobj(source, target)
