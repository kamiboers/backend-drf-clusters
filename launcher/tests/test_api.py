import pytest

from django.test import Client, TestCase
from django.urls import reverse

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
  result = response.json()

  assert response.status_code == 201
  assert response.data == {'cpus': cpus, 'creator': _test_user_uri(user), 'memory': memory}

