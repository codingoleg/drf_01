from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import generics, status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .db import create_test_tables, units
from .models import Units, Users, Jobs
from .serialazers import UnitSerializer, UserSerializer, JobSerializer, UserAuthSerializer
from .utils import get_users_info


class UnitsView(generics.ListAPIView):
    queryset = Units.objects.all().order_by('id')
    serializer_class = UnitSerializer


class UnitRead(generics.RetrieveAPIView):
    queryset = Units.objects.all()
    serializer_class = UnitSerializer


class UnitCreate(generics.CreateAPIView):
    queryset = Units.objects.all()
    serializer_class = UnitSerializer
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)


class UnitUpdateDestroy(generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Units.objects.all()
    serializer_class = UnitSerializer
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)


class UsersView(generics.ListAPIView):
    queryset = Users.objects.all().order_by('id')
    serializer_class = UserSerializer
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)


class UserRead(generics.RetrieveAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)


class UserCreate(generics.CreateAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)


class UserUpdateDestroy(generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)


class JobsView(generics.ListAPIView):
    queryset = Jobs.objects.all().order_by('id')
    serializer_class = JobSerializer
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)


class JobRead(generics.RetrieveAPIView):
    queryset = Jobs.objects.all()
    serializer_class = JobSerializer
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)


class JobCreate(generics.CreateAPIView):
    queryset = Jobs.objects.all()
    serializer_class = JobSerializer
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)


class JobUpdateDestroy(generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Jobs.objects.all()
    serializer_class = JobSerializer
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)


class CreateTestData(APIView):
    """Создание тестовых таблиц"""

    def get(self, request):
        create_test_tables()

        return Response({'detail': 'Тестовые данные созданы'})


class GetMyInfo(APIView):
    """Получение данных о себе"""

    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user_id = request.GET.get('user')
        user = Users.objects.get(id=user_id)
        jobs = user.jobs_set.all().values()
        info = []
        for job in jobs:
            info.append({"username": job['jobname'], "permission": job['permission'], "unit": job['unit']})

        return Response(info)


class GetMyUnitInfo(APIView):
    """Получение данных о пользователях в своем подразделении. Только для прав доступа от 5 и больше."""

    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)

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

    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)

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


@api_view(['POST'])
def signup(request):
    serializer = UserAuthSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)

        return Response({'token': token.key, 'user': serializer.data})

    return Response(serializer.errors, status=status.HTTP_200_OK)


@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])

    if not user.check_password(request.data['password']):
        return Response({"detail": "Пользователь не найден"})

    token, created = Token.objects.get_or_create(user=user)
    serializer = UserAuthSerializer(instance=user)

    return Response({'token': token.key, 'user': serializer.data})
