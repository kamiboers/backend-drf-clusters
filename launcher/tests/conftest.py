import pytest

from rest_framework.test import APIClient

from .utils import random_string
from clusters.models import Cluster
from launcher.models import User


@pytest.fixture(scope='function')
def api_client():
    return APIClient()


@pytest.fixture
def create_user(username=None):
    if not username:
        username = random_string()

    user = create_user_model(username)
    yield user

    user.delete()


@pytest.fixture(scope='function')
def create_cluster(**kwargs):
    def _create_cluster(**kwargs):
        cluster = create_cluster_model(creator=kwargs.get('creator'), cpus=1, memory=1)
        return cluster

    return _create_cluster


def create_user_model(username=None):
    if not username:
        username = random_string()

    user = User(username=username, password='password')
    user.save()
    return user


def create_cluster_model(creator=None, cpus=1, memory=1):
    if creator is None:
        creator = create_user_model()

    cluster = Cluster(creator=creator, cpus=cpus, memory=memory)
    cluster.save()

    return cluster
