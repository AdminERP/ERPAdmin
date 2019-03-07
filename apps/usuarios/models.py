from django.db import models
from django.contrib.auth.models import AbstractUser


class Rol(models.Model):
    nombre = models.CharField(max_length=40)
    descripcion = models.CharField(max_length=40)


class Cargo(models.Model):
    nombre = models.CharField(max_length=40)
    descripcion = models.CharField(max_length=40)
    roles = models.ManyToManyField(Rol, blank=True)


class User(AbstractUser):
    cedula = models.CharField(max_length=10)
    direccion = models.CharField(max_length=20)
    ESTADOS = (
        ('casado', 'Casado'),
        ('soltero', 'Soltero'),
        ('union_libre', 'Unión libre')
    )

    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, blank=True, null=True)
    estado_civil = models.CharField(choices=ESTADOS, max_length=15, blank=True)
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=11)

