import re


class PriceProcessor:
    def __init__(
        self
    ):
        self.price_pattern = r'^\d{3,7}(?:,\d{1,2})*(?:\.\d{1,2})?$'

    def find_price(self, list_values):
        print(list_values)
        for value in list_values[:-2]:
            print(value)
            if re.match(self.price_pattern, str(value)):
                return value

        return None
    