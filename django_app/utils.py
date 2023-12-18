from django.db.models import QuerySet

from .models import Users, Jobs


def get_users_info(info: list, jobs_records: QuerySet):
    """Получение данных о пользователях"""
    for unit_job in jobs_records:

        # Получаем id пользователя по id должности
        jobs_instance = Jobs.objects.get(id=unit_job.id)
        users_instances = jobs_instance.user_jobs.all().values()

        # Получаем все должности по id пользователя
        user_instance = Users.objects.get(id=users_instances[0]['id'])
        jobs_instances = user_instance.jobs_set.all().values()

        # Добавляем имя пользователя в каждую запись с его должностью
        for j in jobs_instances:
            j['username'] = users_instances[0]['username']
            if j not in info:
                info.append(j)

    return info
