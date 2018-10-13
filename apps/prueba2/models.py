from django.db import models
from django.utils import timezone
# Create your models here.


class Job(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    functions = models.TextField()
    has_vacants = models.BooleanField(default=True)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.name

