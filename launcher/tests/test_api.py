import random
import string

from django.test import Client, TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from launcher.models import Cluster, User

client = APIClient()

# TODO: break out tests into separate dir/files, probably create test fixtures
def random_string(length=15):
  letters = string.ascii_lowercase
  return ''.join(random.choice(letters) for i in range(length))

def create_user(username=random_string()):
  user = User(username=username)
  user.save()
  return user

def create_cluster(user, cpus=1, memory=1):
  cluster = Cluster(creator=user, cpus=cpus, memory=memory)
  cluster.save()
  return cluster

def create_client():
  return Client()

def test_fetch_all_clusters_via_api():
  client = create_client()
  user = create_user()
  cluster = create_cluster(user)
  response = client.get('/clusters/', format='json')

  assert response.status_code == 200
  assert len(response.json()) == 1

