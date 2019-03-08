from django.db import models
from django.contrib.auth.models import AbstractUser, Group


class Cargo(Group):
    descripcion = models.CharField(max_length=50)


class Usuario(AbstractUser):
    cedula = models.CharField(max_length=10)
    direccion = models.CharField(max_length=50)
    ESTADOS = (
        ('casado', 'Casado'),
        ('soltero', 'Soltero'),
        ('union_libre', 'Unión libre')
    )
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, blank=True, null=True, related_name='usuario')
    estado_civil = models.CharField(choices=ESTADOS, max_length=15, blank=True)
    fecha_nacimiento = models.DateField(null=True)
    telefono = models.CharField(max_length=11)
