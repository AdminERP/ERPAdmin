from django.db import models
from apps.usuarios.models import User

class OrdenServicio(models.Model):
    servicio_vendido = models.CharField(max_length=100) # Datos Mestros
    encargado = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='encargado_set')
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='cliente_set')# Datos Maestros
    comentarios = models.CharField(max_length=255)

    # Constantes para OrdenServicio
    ASIGNADA = 'AS'
    TRAMITE = 'TR'
    CANCELADA = 'CA'
    CERRADA = 'CE'
    # Fin Constantes

    opciones_estado = (
        (ASIGNADA, 'Asignada'),
        (TRAMITE, 'Tramite'),
        (CANCELADA, 'Cancelada'),
        (CERRADA, 'Cerrada'),
    )
    estado = models.CharField(
        max_length=2,
        choices=opciones_estado,
        default=ASIGNADA,
    )
