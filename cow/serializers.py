from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from cow import models


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class ServerSerializer(ModelSerializer):
    class Meta:
        model = models.IDC
        fields = ('id', 'name')


class AssetSerializer(ModelSerializer):
    class Meta:
        model = models.Assets
        depth = 2
        fields = ('name', 'sn', 'server')


class IDCSerializer(ModelSerializer):
    class Meta:
        model = models.IDC
        # depth = 1
        fields = '__all__'
class BusinessUnitSerializer(ModelSerializer):
    class Meta:
        model = models.BusinessUnit
        fields = '__all__'