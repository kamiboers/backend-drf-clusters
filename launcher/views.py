from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from clusters.models import Cluster
from .serializers import ClusterSerializer


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def cluster_list(request):
    """
    List all clusters belonging to a user, or create a cluster.
    """
    if request.method == 'GET':
        clusters = Cluster.objects.filter(creator__id=request.user.id).all()
        serializer = ClusterSerializer(clusters, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ClusterSerializer(data=request.data)
        if serializer.is_valid() and request.data['creator'] == request.user.id:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def cluster_detail(request, pk):
    """
    Return details of a cluster retrieved by pk.
    """
    try:
        cluster = Cluster.objects.get(pk=pk, creator__id=request.user.id)
    except Cluster.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ClusterSerializer(cluster)
    return Response(serializer.data)
