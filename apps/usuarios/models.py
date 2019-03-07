from django.db import models
from django.contrib.auth.models import AbstractUser


class Rol(models.Model):
    nombre = models.CharField(max_length=40)
    descripcion = models.CharField(max_length=40)

    class Meta:
        verbose_name_plural="Roles"

    def __str__(self):
        return self.nombre

class Cargo(models.Model):
    nombre = models.CharField(max_length=40)
    descripcion = models.CharField(max_length=40)
    roles = models.ManyToManyField(Rol, blank=True)

    class Meta:
        verbose_name_plural ="Cargos"

    def __str__(self):
        return self.nombre

class User(AbstractUser):
    cedula = models.CharField(max_length=10)
    direccion = models.CharField(max_length=20)
    ESTADOS = (
        ('casado', 'Casado'),
        ('soltero', 'Soltero'),
        ('union_libre', 'Unión libre')
    )

    CARGOS = (
        ('C','Coordinador de Servicios'),
        ('O','Operario')
    )

    cargo = models.CharField(max_length=20,choices=CARGOS, blank=True, null=True)
    estado_civil = models.CharField(choices=ESTADOS, max_length=15, blank=True)
    fecha_nacimiento = models.DateField(null=True)
    telefono = models.CharField(max_length=11, null=True)

    def __str__(self):
        return self.get_full_name()


class Cliente(models.Model):
    nombres = models.CharField(max_length=20,null=True, verbose_name="Nombres")
    apellidos = models.CharField(max_length=20,null=True, verbose_name= "Apellidos")
    cedula = models.IntegerField(null=True, verbose_name="Cédula")
    telefono = models.IntegerField(null=True,verbose_name="Teléfono")
    email = models.CharField(max_length=50,null=True, verbose_name="Correo Electrónico")

    class Meta:
        verbose_name_plural="Clientes"

    def __str__(self):
        return self.nombres + " " + self.apellidos;
