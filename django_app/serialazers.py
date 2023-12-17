from rest_framework import serializers

from .models import Units, Users, Jobs


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
