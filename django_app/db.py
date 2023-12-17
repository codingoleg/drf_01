import logging
from collections import OrderedDict

from .models import Units, Users, Jobs

users = ['Ярослав', 'Борис', 'Полина', 'Виталий', 'Григорий', 'Николай', 'Дмитрий',
         'Константин', 'Леонид', 'Анна', 'Зоя', 'Игорь', 'Жанна', 'Евгения', 'Михаил']

units = {
    100: 'IT',
    110: 'Development',
    120: 'Analytics',
    130: 'QA',
    200: 'Хозяйственная часть',
    300: 'Администрация',
    310: 'Бухгалтерия',
    320: 'Отдел кадров'
}

jobs = OrderedDict({
    'Директор': (9, 0),
    'Руководитель IT-отдела': (9, 100),
    'Заместитель директора по административным делам': (9, 300),
    'Teamlead Developer': (9, 110),
    'Senior Developer': (5, 110),
    'Middle Developer': (3, 110),
    'Junior Developer': (1, 110),
    'Middle Analyst': (5, 120),
    'Junior Analyst': (1, 120),
    'Senior QA': (5, 130),
    'Главный бухгалтер': (9, 310),
    'Бухгалтер': (1, 310),
    'Руководитель отдела кадров': (9, 320),
    'Работник отдела кадров': (1, 320),
    'Главный по хозяйственной части': (9, 200),
    'Junior QA': (1, 130)
})


def create_test_tables():
    """Заполнение таблиц новыми данными"""
    for name in users:
        Users(name=name).save()
        logging.info(msg=f'{name} created')

    for _id in units:
        Units(id=_id, name=units[_id]).save()
        logging.info(msg=f'{_id} {units[_id]} created')

    for job in jobs:
        Jobs(name=job, permission=jobs[job][0], unit=jobs[job][1]).save()
        logging.info(msg=f'{job} created')

    for i in range(1, len(users) + 1):
        user = Users.objects.get(pk=i)
        job = Jobs.objects.get(pk=i)
        job.user_jobs.add(user)
        logging.info(msg=f'{job} {user} created')

    # Отдельно добавляем работника с 2 должностями
    user = Users.objects.get(pk=5)
    job = Jobs.objects.get(pk=16)
    job.user_jobs.add(user)
    logging.info(msg=f'{job} {user} created')
