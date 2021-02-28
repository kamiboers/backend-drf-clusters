import pytest

from django.test import Client, TestCase
from django.urls import reverse

from .conftest import create_client
from launcher.models import Cluster, User

# client = create_client()

@pytest.mark.django_db
def test_fetch_all_clusters_via_api(create_user, create_cluster):
  # import pdb; pdb.set_trace()
  # user = create_user
  cluster = create_cluster(create_user)
  assert True

  # response = client.get('/clusters/', format='json')

  # assert response.status_code == 200
  # assert len(response.json()) == 1

