import pytest

from django.test import Client

from launcher.models import Cluster, User

def _test_user_uri(user):
    return f'http://testserver/users/{user.id}/'


@pytest.mark.django_db
def test_fetch_all_clusters_via_api(api_client, create_cluster):
    cluster = create_cluster()
    response = api_client.get('/clusters/', format='json')
    clusters = response.json()['results']

    assert response.status_code == 200
    assert len(clusters) == 1
    assert clusters[0]['creator'] == _test_user_uri(cluster.creator)
    assert clusters[0]['cpus'] == cluster.cpus
    assert clusters[0]['memory'] == cluster.memory


@pytest.mark.django_db
def test_create_cluster_via_api(api_client, create_user):
    user = create_user
    cpus, memory = 12, 34
    params = {'creator': user.uri(), 'cpus': cpus, 'memory': memory}
    response = api_client.post('/clusters/', params, format='json')
    result = response.data

    assert response.status_code == 201
    assert result['cpus'] == cpus
    assert result['creator'] == _test_user_uri(user)
    assert result['memory'] == memory


@pytest.mark.django_db
def test_invalid_create_cluster_parameters_fail_with_message(api_client, create_user):
    user = create_user
    cpus, memory = 1200, 3400
    params = {'creator': user.uri(), 'cpus': cpus, 'memory': memory}
    response = api_client.post('/clusters/', params, format='json')
    error_messages = str(response.json())

    assert response.status_code == 400
    assert 'CPU value must be between 1-16' in error_messages
    assert 'Memory value must be between 1-128' in error_messages


@pytest.mark.django_db
def test_fetch_cluster_by_id(api_client, create_cluster):
    cluster = create_cluster()
    user = cluster.creator
    response = api_client.get(f'/clusters/{cluster.id}/', format='json')

    assert response.status_code == 200
    assert response.data == {
      'id': cluster.id,
      'cpus': cluster.cpus,
      'creator': _test_user_uri(user),
      'memory': cluster.memory
    }

