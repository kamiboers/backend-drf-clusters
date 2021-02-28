import os
import django
import pytest
import random
import string
from rest_framework.test import APIClient

from clusters.settings import BASE_DIR

from launcher.models import Cluster, User


def random_string(length=15):
  letters = string.ascii_lowercase
  return ''.join(random.choice(letters) for i in range(length))


@pytest.fixture
def create_user(username=random_string()):
  user = create_user_model(username)
  yield user

  user.delete()


# @pytest.fixture
# def create_cluster(user=None, cpus=1, memory=1):
#   cluster = create_cluster_model(user, cpus, memory)
#   yield cluster

#   cluster.delete()


def create_client():
  return APIClient()


def create_user_model(username=random_string()):
  user = User(username=username)
  user.save()
  return user


# def create_cluster_model(user=create_user_model(), cpus=1, memory=1):
#   cluster = Cluster(creator=user, cpus=cpus, memory=memory)
#   cluster.save()
#   return cluster
