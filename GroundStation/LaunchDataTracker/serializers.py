from django.contrib.auth.models import User, Group
from rest_framework import serializers

from .models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class LaunchSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LaunchInfo
        fields = ['launch_site', 'flight_computer', 'liftoff_time', 'active_launch', 'id']

class PayloadSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Payload
        fields = ['model_name']

class PeripheralSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PeripheralStatus
        fields = ['p_id', 'p_data', 'id']