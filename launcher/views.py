from rest_framework import permissions, viewsets

from .models import Cluster
from .serializers import ClusterSerializer

class ClusterViewSet(viewsets.ModelViewSet):
  """
  API endpoint that allows clusters to be created or edited.
  """
  queryset = Cluster.objects.all().order_by('-created_at')
  serializer_class = ClusterSerializer
  # permission_classes = permissions.isAuthenticated
