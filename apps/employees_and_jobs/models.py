from django.db import models
from enum import Enum
from django.utils import timezone
# Create your models here.


class Job(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nombre")
    description = models.CharField(max_length=200, verbose_name="Descripción")
    functions = models.TextField(verbose_name="Funciones")
    has_vacants = models.BooleanField(default=True, verbose_name="¿Tiene vacantes?")
    estado = models.BooleanField(default=True, verbose_name="Estado")

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

    name = models.CharField(max_length=200, verbose_name="Nombre")
    id_type = models.CharField(max_length=2, choices=IDENTIFICATION_TYPE, verbose_name="Tipo de identificación")
    identification = models.CharField(max_length=200, verbose_name="Número de identificación")
    address = models.CharField(max_length=200, verbose_name="Dirección")
    email = models.CharField(max_length=200, verbose_name="Correo electrónico")
    telephone = models.CharField(max_length=200, verbose_name="Teléfono")
    eps = models.CharField(max_length=200, verbose_name="EPS")
    pension_fund = models.CharField(max_length=200, verbose_name="Fondo de pensiones")
    severance_fund = models.CharField(max_length=200, verbose_name="Fondo de cesantias")
    bank = models.CharField(max_length=10, choices=BANK_CHOICE, verbose_name="Banco")
    account_number = models.CharField(max_length=200, verbose_name="Número de cuenta")
    salary = models.IntegerField(verbose_name="Salario")
    cargo = models.ForeignKey(Job, on_delete=models.CASCADE, verbose_name="Cargo")
    jefe = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, verbose_name="Jefe Inmediato")
    status = models.BooleanField(default=True, verbose_name="Estado")

    def __str__(self):
        return self.name



