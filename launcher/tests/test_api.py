import pytest

from rest_framework.test import force_authenticate
from rest_framework.test import APIRequestFactory

from .conftest import create_user_model
from launcher.views import cluster_detail, cluster_list


# TODO: test non authenticated calls
# TODO: institute token authentication


factory = APIRequestFactory()


def _get_all_user_clusters(user):
    request = factory.get('/clusters/', format='json')
    force_authenticate(request, user=user)
    response = cluster_list(request)
    clusters = response.data

    return response.status_code, clusters


def _create_user_cluster(user, cpus=1, memory=1):
    params = {'creator': user.id, 'cpus': cpus, 'memory': memory}
    request = factory.post('/clusters/', params, format='json')
    force_authenticate(request, user=user)
    response = cluster_list(request)
    result = response.data

    return response.status_code, result


def _get_user_cluster_by_pk(user, cluster_pk):
    request = factory.get(f'/clusters/{cluster_pk}/', format='json')
    force_authenticate(request, user=user)
    return cluster_detail(request, cluster_pk)


@pytest.mark.django_db
def test_fetch_all_clusters_via_api(api_client, create_cluster):
    cluster = create_cluster()
    status_code, cluster_response = _get_all_user_clusters(cluster.creator)
    user_cluster = cluster_response[0]

    assert status_code == 200
    assert len(cluster_response) == 1
    assert user_cluster['creator'] == cluster.creator.id
    assert user_cluster['cpus'] == cluster.cpus
    assert user_cluster['memory'] == cluster.memory



@pytest.mark.django_db
def test_index_displays_only_user_clusters(api_client, create_user, create_cluster):
    user = create_user
    user2 = create_user_model(username='other_user')
    cluster = create_cluster(creator=user)
    cluster2 = create_cluster(creator=user2)
    status_code, cluster_response = _get_all_user_clusters(user2)

    assert status_code == 200
    assert len(cluster_response) == 1
    assert cluster_response[0]['creator'] == user2.id


@pytest.mark.django_db
def test_create_cluster_via_api(api_client, create_user):
    user = create_user
    cpus, memory = 12, 34
    status_code, created = _create_user_cluster(user, cpus, memory)

    assert status_code == 201
    assert created['cpus'] == cpus
    assert created['creator'] == user.id
    assert created['memory'] == memory


@pytest.mark.django_db
def test_invalid_create_cluster_parameters_fail_with_message(api_client, create_user):
    user = create_user
    cpus, memory = 1200, 3400
    status_code, result = _create_user_cluster(user, cpus, memory)
    error_messages = str(result)

    assert status_code == 400
    assert f'CPU value must be between 1-16. Invalid value: {cpus}' in error_messages
    assert f'Memory value must be between 1-128 GiB. Invalid value: {memory}' in error_messages


@pytest.mark.django_db
def test_fetch_cluster_by_id(api_client, create_cluster):
    cluster = create_cluster()
    user = cluster.creator
    response = _get_user_cluster_by_pk(user, cluster.pk)

    assert response.status_code == 200
    assert response.data == {
      'id': cluster.id,
      'cpus': cluster.cpus,
      'creator': user.id,
      'memory': cluster.memory
    }
