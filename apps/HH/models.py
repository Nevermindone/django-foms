from django.db import models
from django.contrib.auth.models import User


class Queries(models.Model):
    CHOICES = [
        (None, 'Выберите один из пунктов списка'),
        (7, 'Автомобильный бизнес'),
        (4, 'Административный персонал'),
        (5, 'Банки, инвестиции, лизинг'),
        (8, 'Безопасность'),
        (2, 'Бухгалтерия, управленческий учет, финансы предприятия'),
        (16, 'Государственная служба'),
        (9, 'Высший менеджмент'),
        (10, 'Добыча сырья'),
        (26, 'Закупки'),
        (27, 'Домашний персонал'),
        (25, 'Инсталляция и сервис'),
        (1, 'Информационные технологии, интернет, телеком'),
        (11, 'Искусство, развлечения, масс-медиа'),
        (12, 'Консультирование'),
        (3, 'Маркетинг, реклама, PR'),
        (13, 'Медицина, фармацевтика'),
        (14, 'Наука, образование'),
        (15, 'Начало карьеры, студенты'),
        (17, 'Продажи'),
        (18, 'Производство, сельское хозяйство'),
        (29, 'Рабочий персонал'),
        (24, 'Спортивные клубы, фитнес, салоны красоты'),
        (19, 'Страхование'),
        (20, 'Строительство, недвижимость'),
        (21, 'Транспорт, логистика'),
        (22, 'Туризм, гостиницы, рестораны'),
        (6, 'Управление персоналом, тренинги'),
        (23, 'Юристы'),
        (16, 'Государственная служба, некоммерческие организации'),
    ]
    id = models.IntegerField(db_column='id', blank=False, null=False, primary_key=True)
    prof = models.PositiveIntegerField(choices=CHOICES, verbose_name='Профессия', blank=False)
    status = models.IntegerField(default=1, blank=True, null=True)
    dtcreate = models.DateTimeField(auto_now_add=True, db_column='dtCreate')
    dtexec = models.DateTimeField(auto_now=True, null=True, db_column='dtExec')
    cntres = models.IntegerField(db_column='cntRes', blank=True, null=True)
    delete = models.BooleanField(default=True)
    usr = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    delete = models.BooleanField(default=True)

    class Meta:

        managed = True
        db_table = 'queries'


class QuerySearch(models.Model):
    id = models.OneToOneField(Queries, models.DO_NOTHING,
                              db_column='id', primary_key=True, blank=False,
                              null=False, related_name='children')
    text = models.TextField(blank=False, verbose_name="Введите ключевые слова (через ;)")
    #specialization = models.TextField(blank=True, null=True)
    salary_to = models.IntegerField(blank=True, null=True, verbose_name='Введите предельную зп')
    area = models.TextField(blank=True, null=True, verbose_name='Регион')
    experience = models.CharField(max_length=300, blank=True, verbose_name= 'Требуемый опыт работы',
                                  choices=((None, 'Выберите один из пунктов списка'), ('нет', 'нет'), ('от 1 до 3', 'от 1 до 3'), ('от 3 до 6', 'от 3 до 6'), ('от 6', 'от 6'))
                                  )
    skill = models.TextField(blank=True, null=True, verbose_name='Ключевые навыки (через ;)')
    education = models.CharField(max_length=300, blank=True, null=True, verbose_name='Образование',
                                 choices=((None, 'Выберите один из пунктов списка'),
                                          ('не имеет значения', 'не имеет значения'), ('Высшее', 'Высшее'),
                                          ('Бакалавр', 'Бакалавр'), ('Магистр', 'Магистр'), ('Кандидат наук', 'Кандидат наук'),
                                          ('Доктор наук', 'Доктор наук'), ('Незаконченное высшее', 'Незаконченное высшее'),
                                          ('Среднее', 'Среднее'),('Среднее специальное', 'Среднее специальное')))
    citizenship = models.TextField(blank=True, null=True, verbose_name='Гражданство')
    work_ticket = models.TextField(blank=True, null=True, verbose_name='Разрешение на работу')
    age_from = models.TextField(blank=True, null=True, verbose_name='Возраст (от)')
    age_to = models.TextField(blank=True, null=True, verbose_name='Возраст (до)')
    gender = models.CharField(max_length=300, blank=True, null=True, verbose_name= 'Пол',
                              choices=((None, 'Выберите один из пунктов списка'),
                                        ('не имеет значения', 'не имеет значения'),
                                        ('Мужской', 'Мужской'),
                                        ('Женский', 'Женский')))
    employment_full = models.BooleanField(blank=True, null=True, verbose_name='Полная занятость')
    employment_part = models.BooleanField(blank=True, null=True, verbose_name='Частичная занятость')
    employment_project = models.BooleanField(blank=True, null=True, verbose_name='Проектная дестельность')
    employment_volunteer = models.BooleanField(blank=True, null=True, verbose_name='Волонтёрство')
    employment_probation = models.BooleanField(blank=True, null=True, verbose_name='Стажировка')

    schedule_fullday = models.BooleanField(db_column='schedule_fullDay', blank=True, null=True, verbose_name='Полный день')
    schedule_shift = models.BooleanField(blank=True, null=True, verbose_name='Сменный график')
    schedule_flexible = models.BooleanField(blank=True, null=True, verbose_name='Гибкий график')
    schedule_remote = models.BooleanField(blank=True, null=True, verbose_name='Удаленная работа')
    schedule_flyinflyout = models.BooleanField(db_column='schedule_flyInFlyOut', blank=True, null=True, verbose_name='Вахтовый метод')

    language = models.TextField(blank=True, null=True, verbose_name='Язык')
    level = models.CharField(max_length=300, blank=True, null=True, verbose_name='Уровень владения',
                             choices=((None, 'Выберите один из пунктов списка'),
                                        ('не имеет значения', 'не имеет значения'),
                                        ('A1', 'A1'),
                                        ('A2', 'A2'),
                                        ('B1', 'B2'),
                                        ('C1', 'C2'),
                                        ('Родной', 'Родной')))

    searchurl = models.TextField(db_column='searchURL', blank=True, null=True)


    class Meta:
        managed = True
        db_table = 'query_search'


class Urls(models.Model):
    idq = models.ForeignKey(QuerySearch, models.DO_NOTHING, db_column='idQ')
    name = models.TextField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    path = models.TextField(blank=True, null=True)
    isneedcontact = models.BooleanField(db_column='isNeedContact', blank=False, null=False, default=0)
    isdowncontact = models.BooleanField(db_column='isDownContact', blank=False, null=False, default=0)
    salary_goal = models.TextField(blank=True, null=True, verbose_name='Зарплатные ожидания')
    last_job = models.TextField(blank=True, null=True, verbose_name='Последнее место работы')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    old = models.BooleanField(default=False)


    class Meta:
        managed = True
        db_table = 'urls'



