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

    id_type = models.CharField(max_length=2, choices=IDENTIFICATION_TYPE, verbose_name="Tipo de identificación")
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
    eps = models.CharField(max_length=200, verbose_name="EPS")
    pension_fund = models.CharField(max_length=200, verbose_name="Fondo de pensiones")
    severance_fund = models.CharField(max_length=200, verbose_name="Fondo de cesantias")
    bank = models.CharField(max_length=10, choices=BANK_CHOICE, verbose_name="Banco")
    account_number = models.CharField(max_length=200, verbose_name="Número de cuenta")
    salary = models.IntegerField(verbose_name="Salario", null=True)
    jefe = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, verbose_name="Jefe Inmediato")

    @staticmethod
    def consultar_usuarios():
        try:
            queryset = Usuario.objects.all()
            return queryset
        except Usuario.DoesNotExist:
            return None
            
    @staticmethod
    def consultar_subordinados(id_jefe):
        try:
            queryset = Usuario.objects.filter(jefe__id=id_jefe)
            return queryset
        except Usuario.DoesNotExist:
            return None

    class Meta:
        permissions = (
            ('view_usuarios', 'Puede consultar los usuarios'),
            ('change_password', 'Puede reestablecer las contraseñas de los usuarios'),
            ('activate_usuario', 'Puede activar/desactivar usuarios'),
        )

    def __str__(self):
        return self.get_full_name()
