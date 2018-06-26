from django.contrib.auth.models import User, Group
# from cow.serializers import UserSerializer, AssetSerializer, ServerSerializer,IDCSerializer
from cow import serializers
# from rest_framework import serializers
from rest_framework import viewsets
from cow import models


# class UserViewSet(viewsets.ModelViewSet):
#     queryset = myauth.UserProfile.objects.all().order_by('-date_joined')
#     serializer_class = UserSerializer

class GroupSet(viewsets.ModelViewSet):
    class Meta:
        model = Group
        fields = ('url', 'name')


class IDCViewSet(viewsets.ModelViewSet):
    queryset = models.IDC.objects.all()
    serializer_class = serializers.IDCSerializer


class AssetViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Asset to be viewed or edited.
    """
    queryset = models.Assets.objects.all()
    serializer_class = serializers.AssetSerializer


class BusinessUnitSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Asset to be viewed or edited.
    """
    queryset = models.BusinessUnit.objects.all()
    serializer_class = serializers.BusinessUnitSerializer
