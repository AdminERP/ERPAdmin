from django.db import models

class OrdenServicio(models.Model):
    servicio_vendido = models.CharField(max_length=100) # Datos Mestros
    encargado = models.CharField(max_length=100) # Datos Maestros
    cliente = models.CharField(max_length=100) # Datos Maestros
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
