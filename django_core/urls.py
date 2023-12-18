"""
URL configuration for django_core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, username='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), username='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path

from django_app.views import UnitsView, UnitCreate, UnitRead, UnitUpdateDestroy
from django_app.views import UsersView, UserCreate, UserRead, UserUpdateDestroy
from django_app.views import JobsView, JobCreate, JobRead, JobUpdateDestroy
from django_app.views import CreateTestData, GetMyInfo, GetMyUnitInfo, GetSubUnitInfo
from django_app.views import signup, login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/create_test_tables/', CreateTestData.as_view()),

    # Units CRUD
    path('api/v1/units_view/', UnitsView.as_view()),
    path('api/v1/unit_view/<int:pk>/', UnitRead.as_view()),
    path('api/v1/unit/', UnitCreate.as_view()),
    path('api/v1/unit/<int:pk>/', UnitUpdateDestroy.as_view()),

    # Users CRUD
    path('api/v1/users_view/', UsersView.as_view()),
    path('api/v1/user_view/<int:pk>/', UserRead.as_view()),
    path('api/v1/user/', UserCreate.as_view()),
    path('api/v1/user/<int:pk>/', UserUpdateDestroy.as_view()),

    # Jobs CRUD
    path('api/v1/jobs_view/', JobsView.as_view()),
    path('api/v1/job_view/<int:pk>/', JobRead.as_view()),
    path('api/v1/job/', JobCreate.as_view()),
    path('api/v1/job/<int:pk>/', JobUpdateDestroy.as_view()),

    # Get info
    path('api/v1/get_my_info/', GetMyInfo.as_view()),
    path('api/v1/get_my_unit_info/', GetMyUnitInfo.as_view()),
    path('api/v1/get_subunit_info/', GetSubUnitInfo.as_view()),

    # Auth
    re_path('signup/', signup),
    re_path('login/', login),
]
