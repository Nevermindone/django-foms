def contact_handler(down, need):
    return down+need


class DataListsCreate:

    def __init__(self, query_set):
        self.query_set = query_set
        self.dict_contact = {0: 'Контакты не запрошены',
                             1: 'Обработка контактов',
                             2: 'Контакты предоставлены'}

    def query_to_lists(self):
        idq = list(self.query_set.values_list('id', flat=True))
        salary_goal = list(self.query_set.values_list('salary_goal', flat=True))
        last_job = list(self.query_set.values_list('last_job', flat=True))
        name = list(self.query_set.values_list('name', flat=True))
        url = list(self.query_set.values_list('url', flat=True))
        path = list(self.query_set.values_list('path', flat=True))
        isneedcontact = list(self.query_set.values_list('isneedcontact', flat=True))
        isdowncontact = list(self.query_set.values_list('isdowncontact', flat=True))
        listt = []
        dct = {}
        for i in range(len(idq)):
            dct['idq'] = idq[i]
            dct['name'] = name[i]
            dct['url'] = url[i]
            dct['path'] = path[i]
            dct['isdowncontact'] = self.dict_contact[contact_handler(isdowncontact[i], isneedcontact[i])]
            dct['salary_goal'] = salary_goal[i].replace('&nbsp;', ' ') if salary_goal[i] else None
            dct['last_job'] = last_job[i].replace('&nbsp;', ' ') if last_job[i] else None
            listt.append(dct)
            dct = {}
        return listt
