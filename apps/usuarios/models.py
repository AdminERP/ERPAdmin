from django.contrib.auth.models import AbstractUser, Group
from django.core.validators import MinLengthValidator
from django.db import models


class Cargo(Group):
    descripcion = models.TextField(max_length=500)

    @staticmethod
    def consultar_cargos():
        try:
            queryset = Cargo.objects.all()
            return queryset
        except Cargo.DoesNotExist:
            return None

    class Meta:
        permissions = (
            ('view_cargos', 'Puede ver los cargos'),
        )


class Usuario(AbstractUser):
    cedula = models.CharField(max_length=10, unique=True,
                              validators=[MinLengthValidator(8, 'Asegurese que la cédula tenga al menos 8 dígitos')])
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

    @staticmethod
    def consultar_usuarios():
        try:
            queryset = Usuario.objects.all()
            return queryset
        except Usuario.DoesNotExist:
            return None

    class Meta:
        permissions = (
            ('view_usuarios', 'Puede consultar los usuarios'),
            ('change_password', 'Puede reestablecer las contraseñas de los usuarios'),
            ('activate_usuario', 'Puede activar/desactivar usuarios'),
        )