import os


class RarHandler:
    @staticmethod
    def process(input_file, output):
        os.popen(f"unrar e {input_file} {output} -y").read()
