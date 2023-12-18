from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Units, Jobs, Users


class UserAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Units
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jobs
        fields = '__all__'
