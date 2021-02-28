from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    def uri(self):
        return f'http://127.0.0.1:8000/users/{self.id}/'


class Cluster(models.Model):
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    cpus = models.IntegerField(verbose_name="Number of CPUs allocated for this cluster.")
    memory = models.IntegerField(verbose_name="Memory allocated for this cluster, in bytes.")
