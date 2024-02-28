import pandas as pd
from pandas import ExcelWriter


class ExcelCreator:
    def __init__(self, responses):
        self.responses = responses
        self.response_columns = ['description', 'price', 'file', 'page', 'archive_name', 'error_message']

    def make_excel(self, filename):
        responses_dicts_list = [response.to_dict() for response in self.responses]
        df = pd.DataFrame(responses_dicts_list)
        df_main = df[(df['main_data_object'] == True)]
        df_error = df[(df['error_data_object'] == True)]
        df_other = df[(df['error_data_object'] == False) & (df['main_data_object'] == False)]
        df_main[self.response_columns].to_excel(filename, sheet_name='Данные')
        with ExcelWriter(filename, mode='a') as writer:
            df_error[self.response_columns].to_excel(writer, sheet_name='Ошибки')
        with ExcelWriter(filename, mode='a') as writer:
            df_other[self.response_columns].to_excel(writer, sheet_name='Прочее')
