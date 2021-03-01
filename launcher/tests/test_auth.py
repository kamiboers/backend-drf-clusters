import pytest

from django.test import Client
from rest_framework.test import APIRequestFactory

from launcher.views import cluster_list


# TODO: remove duplication
client = Client()
factory = APIRequestFactory()


# TODO: pull out as shared method from test_api
def _get_all_user_clusters(user, token_header=''):
    request = factory.get('/clusters/', format='json', HTTP_AUTHORIZATION=token_header)
    response = cluster_list(request)
    clusters = response.data

    return response.status_code, clusters


def _login_user(username, password):
    params = {'username': username, 'password': password}
    response = client.post('/auth/', data=params)
    return response


@pytest.mark.django_db
def test_obtain_token_via_api(api_client, create_user):
    user = create_user
    password = 'bestpassword123'
    user.set_password(password)
    user.save()

    response = _login_user(user.username, password)

    assert response.status_code == 200
    assert response.data['token']


@pytest.mark.django_db
def test_obtain_token_fails_with_bad_credentials(api_client, create_user):
    user = create_user
    response = _login_user(user.username, 'wrong_password')

    assert response.status_code == 400
    assert 'Unable to log in with provided credentials' in str(response.data)


@pytest.mark.django_db
def test_clusters_resource_unavailable_without_token_header(api_client, create_cluster):
    cluster = create_cluster()
    status_code, _response = _get_all_user_clusters(cluster.creator)

    assert status_code == 401


@pytest.mark.django_db
def test_clusters_resource_accessible_with_token_header(api_client, create_user, create_cluster):
    cluster = create_cluster()
    user = cluster.creator
    password = 'bestpassword123'
    user.set_password(password)
    user.save()
    token_response = _login_user(user.username, password)
    token_header = f'Token {token_response.data.get("token")}'
    status_code, response = _get_all_user_clusters(user, token_header=token_header)

    assert status_code == 200
    assert len(response) == 1
