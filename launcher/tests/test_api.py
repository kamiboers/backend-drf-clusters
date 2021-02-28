import pytest

from django.test import Client, TestCase
from django.urls import reverse

from launcher.models import Cluster, User


@pytest.mark.django_db
def test_fetch_all_clusters_via_api(api_client, create_user, create_cluster):
  user = create_user
  cluster = create_cluster(creator=user)

  response = api_client.get('/clusters/', format='json')
  clusters = response.json()['results']

  assert response.status_code == 200
  assert len(clusters) == 1
  assert clusters[0]['creator'] == f'http://testserver/users/{user.id}/'
  assert clusters[0]['cpus'] == cluster.cpus
  assert clusters[0]['memory'] == cluster.memory

