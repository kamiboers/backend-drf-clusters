from rest_framework import permissions, viewsets

from .models import Cluster, User
from .serializers import ClusterSerializer, UserSerializer

class ClusterViewSet(viewsets.ModelViewSet):
  """
  API endpoint that allows clusters to be created or edited.
  """
  queryset = Cluster.objects.all()
  serializer_class = ClusterSerializer
  # permission_classes = permissions.isAuthenticated

class UserViewSet(viewsets.ModelViewSet):
  """
  API endpoint that displays existing Users
  """
  queryset = User.objects.all()
  serializer_class = UserSerializer
  # permission_classes = permissions.isAuthenticated
