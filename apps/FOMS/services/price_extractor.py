import re


class PriceProcessor:
    def __init__(
        self
    ):
        self.price_pattern = r'^\d{3,7}(?:,\d{1,2})*(?:\.\d{1,2})?$'

    # def find_price(self, list_values):
    #     for value in list_values[:-2]:
    #         if re.match(self.price_pattern, str(value)):
    #             return value
    #
    #     return None

    def find_price(self, list_values):
        possible_price_values = []
        for value in list_values[:-2]:
            if re.match(self.price_pattern, str(value)):
                possible_price_values.append(str(value))
        value = ', '.join(possible_price_values)
        return value
    