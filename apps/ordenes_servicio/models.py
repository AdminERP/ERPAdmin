from django.db import models
from apps.usuarios.models import *
from apps.datosmaestros.models.dato import DatoModel
from datetime import datetime

class OrdenServicio(models.Model):
    servicio_vendido = models.ForeignKey(DatoModel, on_delete=models.CASCADE, blank=True, null=False,
                                    limit_choices_to= {'categoria__nombre':"servicios"},
                                    related_name='servicio_set', verbose_name="Servicio")# Datos Maestros

    coordinador = models.ForeignKey(Usuario,
                                    # Solo los coordinadores pueden crear
                                    limit_choices_to= {'cargo__permissions__codename':"add_ordenservicio"},
                                    on_delete=models.CASCADE, blank=True, null=False,
                                    related_name='coordinador_set', verbose_name="Coordinador")

    encargado = models.ForeignKey(Usuario,
                                  # Solo los operarios pueden encargarse
                                  limit_choices_to={'cargo__permissions__codename':'execute_ordenservicio'},
                                  on_delete=models.CASCADE, blank=True, null=False,
                                  related_name='encargado_set', verbose_name="Encargado")

    cliente = models.ForeignKey(DatoModel, on_delete=models.CASCADE, blank=True, null=False,
                                related_name='cliente_set', verbose_name="Cliente")# Datos Maestros

    comentarios = models.TextField(max_length=255)
    fecha_creacion = models.DateTimeField(default=datetime.now, blank=True, verbose_name="Fecha de Creación")
    fecha_atencion = models.DateTimeField(null=True, verbose_name="Fecha de Atención")
    valor = models.PositiveIntegerField(null=False, default=0)

    # Constantes para OrdenServicio
    ASIGNADA = 'AS'
    TRAMITE = 'TR'
    CANCELADA = 'CA'
    CERRADA = 'CE'
    COBRADA = 'CO'
    # Fin Constantes

    opciones_estado = (
        (ASIGNADA, 'Asignada'),
        (TRAMITE, 'Tramite'),
        (CANCELADA, 'Cancelada'),
        (CERRADA, 'Cerrada'),
        (COBRADA,'Cobrada')
    )
    estado = models.CharField(
        max_length=2,
        choices=opciones_estado,
        default=ASIGNADA,
    )

    class Meta:
        verbose_name_plural = "Ordenes de Servicio"
        permissions = (
            ('execute_ordenservicio',"Puede Atender una Orden de Servicio"),
            ('close_ordenservicio', "Puede Cerrar una Orden de Servicio"),
            ("cancel_ordenservicio", "Puede Cancelar una Orden de Servicio"),
            ("view_ordenservicio", "Puede Ver Ordenes de Servicio"),
        )

    def get_data(usuario):
        if isinstance(usuario,Usuario):
            if usuario.has_perm("ordenes_servicio.add_ordenservicio"):
                try:
                    ordenes = OrdenServicio.objects.filter(coordinador=usuario.id)
                    return ordenes
                except OrdenServicio.DoesNotExist:
                    return None
            elif usuario.has_perm("ordenes_servicio.execute_ordenservicio"):
                try:
                    ordenes = OrdenServicio.objects.filter(encargado=usuario.id)
                    return ordenes
                except OrdenServicio.DoesNotExist:
                    return None
        return None

    def __str__(self):
        return "Orden de servicio: "+str(self.id)
