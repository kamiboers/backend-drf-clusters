import pytest

from rest_framework.test import force_authenticate
from rest_framework.test import APIRequestFactory

from .conftest import create_user_model


factory = APIRequestFactory()

def _build_auth_request(username, password):
    params = {'username': username, 'password': password}
    request = factory.post('/token/login/', params, format='json')
    return request


def _login_user(username, password):
    request = _build_auth_request(username, password)
    response = login(request, username, password)
    result = response.data

    return response.status_code, result


@pytest.mark.django_db
def test_login_via_api(api_client, create_user):
    user = create_user
    status_code, created = _login_user(user.username, user.password)

    assert status_code == 200


@pytest.mark.django_db
def test_invalid_create_cluster_parameters_fail_with_message(api_client, create_user):
    user = create_user
    cpus, memory = 1200, 3400
    status_code, result = _create_user_cluster(user, cpus, memory)
    error_messages = str(result)

    assert status_code == 400
    assert f'CPU value must be between 1-16. Invalid value: {cpus}' in error_messages
    assert f'Memory value must be between 1-128 GiB. Invalid value: {memory}' in error_messages
