import pytest

from django.test import Client
from rest_framework.test import force_authenticate
from rest_framework.test import APIRequestFactory

from launcher.models import Cluster, User
from launcher.views import cluster_detail, cluster_list

factory = APIRequestFactory()

# TODO: clean up request/auth functionality
# TODO: test non authenticated calls
# TODO: institute token authentication

@pytest.mark.django_db
def test_fetch_all_clusters_via_api(api_client, create_cluster):
    cluster = create_cluster()
    request = factory.get('/clusters/', format='json')
    force_authenticate(request, user=cluster.creator)
    response = cluster_list(request)
    clusters = response.data

    assert response.status_code == 200
    assert len(clusters) == 1
    assert clusters[0]['creator'] == cluster.creator.id
    assert clusters[0]['cpus'] == cluster.cpus
    assert clusters[0]['memory'] == cluster.memory


@pytest.mark.django_db
def test_create_cluster_via_api(api_client, create_user):
    user = create_user
    cpus, memory = 12, 34
    params = {'creator': user.id, 'cpus': cpus, 'memory': memory}
    request = factory.post('/clusters/', params, format='json')
    force_authenticate(request, user=user)
    response = cluster_list(request)
    created = response.data

    assert response.status_code == 201
    assert created['cpus'] == cpus
    assert created['creator'] == user.id
    assert created['memory'] == memory


@pytest.mark.django_db
def test_invalid_create_cluster_parameters_fail_with_message(api_client, create_user):
    user = create_user
    cpus, memory = 1200, 3400
    params = {'creator': user.id, 'cpus': cpus, 'memory': memory}
    request = factory.post('/clusters/', params, format='json')
    force_authenticate(request, user=user)
    response = cluster_list(request)
    error_messages = str(response.data)

    assert response.status_code == 400
    assert 'CPU value must be between 1-16' in error_messages
    assert 'Memory value must be between 1-128' in error_messages


@pytest.mark.django_db
def test_fetch_cluster_by_id(api_client, create_cluster):
    cluster = create_cluster()
    user = cluster.creator
    request = factory.get(f'/clusters/{cluster.id}/', format='json')
    force_authenticate(request, user=cluster.creator)
    response = cluster_detail(request, cluster.id)

    assert response.status_code == 200
    assert response.data == {
      'id': cluster.id,
      'cpus': cluster.cpus,
      'creator': user.id,
      'memory': cluster.memory
    }

