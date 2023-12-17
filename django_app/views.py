from django.db.models import Q, QuerySet
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Units, Users, Jobs
from .serialazers import UnitSerializer, UserSerializer, JobSerializer
from .db import create_test_tables, units


class UnitsView(generics.ListAPIView):
    queryset = Units.objects.all().order_by('id')
    serializer_class = UnitSerializer


class UnitRead(generics.RetrieveAPIView):
    queryset = Units.objects.all()
    serializer_class = UnitSerializer


class UnitCreate(generics.CreateAPIView):
    queryset = Units.objects.all()
    serializer_class = UnitSerializer


class UnitUpdateDestroy(generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Units.objects.all()
    serializer_class = UnitSerializer


class UsersView(generics.ListAPIView):
    queryset = Users.objects.all().order_by('id')
    serializer_class = UserSerializer


class UserRead(generics.RetrieveAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer


class UserCreate(generics.CreateAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer


class UserUpdateDestroy(generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer


class JobsView(generics.ListAPIView):
    queryset = Jobs.objects.all().order_by('id')
    serializer_class = JobSerializer


class JobRead(generics.RetrieveAPIView):
    queryset = Jobs.objects.all()
    serializer_class = JobSerializer


class JobCreate(generics.CreateAPIView):
    queryset = Jobs.objects.all()
    serializer_class = JobSerializer


class JobUpdateDestroy(generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Jobs.objects.all()
    serializer_class = JobSerializer


class CreateTestData(APIView):
    """Создание тестовых таблиц"""
    def get(self, request):
        create_test_tables()

        return Response({'detail': 'Тестовые данные созданы'})


class GetMyInfo(APIView):
    """Получение данных о себе"""
    def get(self, request):
        user_id = request.GET.get('user')
        user = Users.objects.get(id=user_id)
        jobs = user.jobs_set.all().values()
        info = []
        for job in jobs:
            info.append({"name": job['name'], "permission": job['permission'], "unit": job['unit']})

        return Response(info)


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
            j['username'] = users_instances[0]['name']
            info.append(j)

    return info


class GetMyUnitInfo(APIView):
    """Получение данных о пользователях в своем подразделении. Только для прав доступа =<5."""
    def get(self, request):
        user_id = request.GET.get('user')
        user = Users.objects.get(id=user_id)
        jobs = user.jobs_set.all().values()
        info = []
        for job in jobs:
            if job['permission'] < 5:
                info.append({"detail": f"Недостаточно прав доступа для отдела {units[job['unit']]}"})
            else:
                jobs_records = Jobs.objects.filter(unit=job['unit'])
                get_users_info(info, jobs_records)

        return Response(info)


class GetSubUnitInfo(APIView):
    """Получение данных о пользователях в своем и дочерних подразделенях.
    Только для головных подразделений, код которых кратен 100."""
    def get(self, request):
        user_id = request.GET.get('user')
        user = Users.objects.get(id=user_id)
        jobs = user.jobs_set.all().values()
        info = []

        for job in jobs:
            if job['unit'] % 100:
                info.append({"detail": f"Недостаточно прав доступа для отдела {units[job['unit']]}"})
            else:
                jobs_records = Jobs.objects.filter(Q(unit__gte=job['unit']) & Q(unit__lt=job['unit'] + 100))
                get_users_info(info, jobs_records)

        return Response(info)
