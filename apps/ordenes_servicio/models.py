from django.db import models
from apps.usuarios.models import *
from datetime import datetime

class OrdenServicio(models.Model):
    servicio_vendido = models.CharField(max_length=100) # Datos Mestros

    coordinador = models.ForeignKey(User,
                                  limit_choices_to={'cargo': 'C'},  # Solo los coordinadores pueden crear
                                  on_delete=models.CASCADE, blank=True, null=False,
                                  related_name='coordinador_set', verbose_name="Coordinador")

    encargado = models.ForeignKey(User,
                                  limit_choices_to={'cargo':'O'}, #Solo los operarios pueden encargarse
                                  on_delete=models.CASCADE, blank=True, null=False,
                                  related_name='encargado_set', verbose_name="Encargado")

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, blank=True, null=False,
                                related_name='cliente_set', verbose_name="Cliente")# Datos Maestros

    comentarios = models.TextField(max_length=255)

    fecha_creacion = models.DateTimeField(default=datetime.now, blank=True, verbose_name="Fecha de Creación")
    fecha_atencion = models.DateTimeField(null=True, verbose_name="Fecha de Atención")
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
    valor = models.PositiveIntegerField(null=False, default=0)

    class Meta:
        verbose_name_plural = "Ordenes de Servicio"

    def get_data(usuario):
        cargo = User.objects.get(id=usuario.id).cargo
        if cargo == 'C':
            try:
                ordenes = OrdenServicio.objects.filter(coordinador=usuario.id)
                return ordenes
            except OrdenServicio.DoesNotExist:
                return None
        elif cargo == 'O':
            try:
                ordenes = OrdenServicio.objects.filter(encargado=usuario.id)
                return ordenes
            except OrdenServicio.DoesNotExist:
                return None

    def __str__(self):
        return "Orden de servicio: "+str(self.id)
