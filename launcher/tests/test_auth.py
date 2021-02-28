import pytest

from django.test import Client
from rest_framework.authtoken import views as auth_views
from rest_framework.test import APIRequestFactory

from launcher.models import User
from launcher.views import cluster_detail, cluster_list



client = Client()

factory = APIRequestFactory()

# todo - move to utils or conftest
def _get_all_user_clusters(user, headers={}):
    request = factory.get('/clusters/', format='json', headers=headers)
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


@pytest.mark.django_db
def test_clusters_resource_unavailable_without_token_header(api_client, create_cluster):
    cluster = create_cluster()
    status_code, response = _get_all_user_clusters(cluster.creator)

    assert status_code == 401


@pytest.mark.django_db
def test_clusters_resource_accessible_with_token_header(api_client, create_user):
    user = create_user
    password = 'bestpassword123'
    user.set_password(password)
    user.save()
    token_response = _login_user(user.username, password)
    headers = {
        'Authorization': f'Token {token_response.data["token"]}'
    }

    import pdb; pdb.set_trace()
    status_code, response = _get_all_user_clusters(user, headers=headers)
    assert status_code == 200


# @pytest.mark.django_db
# def test_invalid_create_cluster_parameters_fail_with_message(api_client, create_user):
#     user = create_user
#     cpus, memory = 1200, 3400
#     status_code, result = _create_user_cluster(user, cpus, memory)
#     error_messages = str(result)

#     assert status_code == 400
#     assert f'CPU value must be between 1-16. Invalid value: {cpus}' in error_messages
#     assert f'Memory value must be between 1-128 GiB. Invalid value: {memory}' in error_messages
