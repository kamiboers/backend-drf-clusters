from rest_framework import serializers

from .models import Cluster, User

class ClusterSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Cluster
    fields = ['cpus', 'creator', 'memory']

class UserSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'username']
