from django.test import Client, TestCase
from django.urls import reverse

from launcher.models import Cluster, User


# TODO: break out tests into separate dir/files, probably create test fixtures
def create_user(username='username'):
  return User.create(username='username')

def create_cluster(user_id, cpus=1, memory=1):
  return Cluster.create(creator=user_id, cpus=cpus, memory=memory)

def create_client():
  return Client()

def test_fetch_all_clusters_via_api():
  client = create_client()
  user = create_user()
  cluster = create_cluster(user_id=user.id)
  response = client.get(reverse('clusters:index'))
  
  assert response.status_code == 200
  assert response.content == []

