from django.db import models
from apps.usuarios.models import *

class OrdenServicio(models.Model):
    servicio_vendido = models.CharField(max_length=100) # Datos Mestros
    encargado = models.ForeignKey(User,
                                  limit_choices_to={'cargo':'O'}, #Solo los operarios pueden encargarse
                                  on_delete=models.CASCADE, blank=True, null=True,
                                  related_name='encargado_set', verbose_name="Encargado")
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, blank=True, null=True,
                                related_name='cliente_set', verbose_name="Cliente")# Datos Maestros
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

    class Meta:
        verbose_name_plural = "Ordenes de Servicio"

    def __str__(self):
        return "Orden de servicio: "+str(self.id)
