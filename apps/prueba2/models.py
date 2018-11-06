from django.db import models
from enum import Enum
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


class Employee(models.Model):

    IDENTIFICATION_TYPE = (
        ('CC', 'Cedula de ciudadania'),
        ('PP', 'Pasaporte')
    )

    BANK_CHOICE = (
        ('BANAGRARIO', 'Banco Agrario de Colombia'),
        ('AVVILLAS', 'Banco AV Villas'),
        ('BCSC', 'Banco Caja Social'),
        ('OCCIDENTE', 'Banco de Occidente'),
        ('POPULAR', 'Banco Popular'),
        ('BCOLOMBIA', 'Bancolombia'),
        ('BBVA', 'Banco BBVA'),
        ('BANBOGOTA', 'Banco de Bogota'),
        ('CITIBANK', 'Citibank Colombia'),
        ('COLPATRIA', 'Scotiabank Colpatria'),
        ('DAVIVIENDA', 'Davivienda')
    )

    name = models.CharField(max_length=200)
    id_type = models.CharField(max_length=2, choices=IDENTIFICATION_TYPE)
    identification = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    telephone = models.CharField(max_length=200)
    eps = models.CharField(max_length=200)
    pension_fund = models.CharField(max_length=200)
    severance_fund = models.CharField(max_length=200)
    bank = models.CharField(max_length=10, choices=BANK_CHOICE)
    account_number = models.CharField(max_length=200)
    salary = models.IntegerField()
    cargo = models.ForeignKey(Job, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name



