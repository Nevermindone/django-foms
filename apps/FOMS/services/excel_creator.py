import pandas as pd


class ExcelCreator:
    def __init__(self, responses):
        self.responses = responses

    def make_excel(self, filename):
        responses_dicts_list = [response.to_dict() for response in self.responses]
        df = pd.DataFrame(responses_dicts_list)
        print(responses_dicts_list)
        df = df[(df['description'].notna()) | (df['has_error']==True)]
        df.to_excel(filename)
