from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError


def _validate_cpus(value):
    if not 1 <= value <= 16:
        raise ValidationError(f'CPU value must be between 1-16. Invalid value: {value}')
    

def _validate_memory(value):
    if not 1 <= value <= 128:
        raise ValidationError(f'Memory value must be between 1-128 GiB. Invalid value: {value}')


class Cluster(models.Model):
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    cpus = models.IntegerField(
        verbose_name="Number of CPUs allocated for this cluster.",
        validators=[_validate_cpus]
    )
    memory = models.IntegerField(
        verbose_name="Memory allocated for this cluster, in GiB.",
        validators=[_validate_memory]
    )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Cluster, self).save(*args, **kwargs)
