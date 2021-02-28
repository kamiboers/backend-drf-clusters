import pytest

from django.core.exceptions import ValidationError

from .conftest import create_cluster_model
from launcher.models import Cluster, User

def _test_user_uri(user):
    return f'http://testserver/users/{user.id}/'


@pytest.mark.django_db
def test_cluster_invalid_without_creator():
    with pytest.raises(ValidationError) as error:
      cluster = Cluster(creator=None, cpus=1, memory=1)
      cluster.save()

    assert [*error.value.error_dict.keys()] == ['creator']


@pytest.mark.django_db
def test_create_cluster_validates_cpu_gt_zero():
    with pytest.raises(ValidationError) as error:
      create_cluster_model(cpus=0)

    assert [*error.value.error_dict.keys()] == ['cpus']


@pytest.mark.django_db
def test_create_cluster_validates_cpu_lte_16():
    with pytest.raises(ValidationError) as error:
      create_cluster_model(cpus=50)

    assert [*error.value.error_dict.keys()] == ['cpus']


@pytest.mark.django_db
def test_create_cluster_validates_memory_gt_zero():
    with pytest.raises(ValidationError) as error:
      create_cluster_model(memory=0)

    assert [*error.value.error_dict.keys()] == ['memory']


@pytest.mark.django_db
def test_create_cluster_validates_memory_lte_128():
    with pytest.raises(ValidationError) as error:
      create_cluster_model(memory=500)

    assert [*error.value.error_dict.keys()] == ['memory']

