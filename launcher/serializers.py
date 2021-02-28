from rest_framework import serializers

from clusters.models import Cluster
from .models import User


class ClusterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cluster
        fields = ['id', 'cpus', 'creator', 'memory']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
