class DescriptionProcessor:
    def __init__(
            self,
            keyword
    ):
        self.keyword = keyword

    def find_and_process_description(self, list_values):
        value = self.find_value(list_values)
        if value:
            value = self.process_value(value)
        else:
            value = None
        return value

    @staticmethod
    def process_value(value):
        value = value.replace('\n', ' ')
        return value

    def find_value(self, list_values):
        for value in list_values[:-2]:
            if self.keyword in str(value):
                return value
        return None
