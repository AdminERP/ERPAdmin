""" Modelos propios modulo Compras """

from django.db import models

from apps.datosmaestros.models import DatoModel
from apps.usuarios.models import Usuario
from django.core.mail import send_mail, EmailMessage
from django.conf import settings

class SolicitudCompra(models.Model):

    PENDIENTE = 'pendiente'
    APROBADO_JEFE = 'aprobado_jefe'
    APROBADO_GERENTE = 'aprobado_gerente'
    RECHAZADO = 'rechazada'

    ESTADOS = [
        (PENDIENTE, 'Pendiente aprobacion'),
        (APROBADO_JEFE, 'Aprobado jefe'),
        (APROBADO_GERENTE, 'Aprobado gerente'),
        (RECHAZADO, 'Rechazada'),
    ]

    justificacion = models.CharField(max_length=1000)
    fecha_realizada = models.DateField(auto_now_add=True)
    fecha_esperada = models.DateField()

    estado_aprobacion = models.CharField(
        max_length=16, choices=ESTADOS, default=PENDIENTE)

    solicitante = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, null=True)
    cantidad = models.SmallIntegerField()
    articulo = models.ForeignKey(DatoModel, on_delete=models.CASCADE)

    class Meta:
        permissions = (
            ("view_solicitudcompra", "Puede ver una solicitud de compra"),
            ("autorizar_solicitud", "Puede autorizar una solicitud"),
            ("rechazar_solicitud", "Puede rechazar una solicitud"),
        )

    def __str__(self):
        return '%s' % (self.id)


class Cotizacion(models.Model):

    # Representa desde 0,00 hasta (10E15)-1,99 en pesos.
    total = models.DecimalField(max_digits=17, decimal_places=2)
    fecha_realizada = models.DateField()

    proveedor = models.ForeignKey(DatoModel, on_delete=models.CASCADE)
    solicitud = models.ForeignKey(SolicitudCompra, on_delete=models.CASCADE)
    
    class Meta:
        permissions = (
            ("view_cotizaciones", "Puede ver una cotizacion"),
        )
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('compras:cotizaciones_listar', kwargs={'pk': self.solicitud.id})


class OrdenCompra(models.Model):

    PENDIENTE = 'pendiente'
    APROBADO_GERENTE = 'aprobado_gerente'
    RECHAZADO = 'rechazada'

    ESTADOS = [
        (PENDIENTE, 'Pendiente aprobacion'),
        (APROBADO_GERENTE, 'Aprobado gerente'),
        (RECHAZADO, 'Rechazada'),
    ]

    cotizacion = models.ForeignKey(Cotizacion, on_delete=models.CASCADE)

    fecha_realizada = models.DateField(auto_now_add=True)
    fecha_esperada = models.DateField()

    estado_aprobacion = models.CharField(
        max_length=16, choices=ESTADOS, default=PENDIENTE)
    
    class Meta:
        permissions = (
            ("view_ordencompra", "Puede ver una orden de compra"),
            ("autorizar_orden", "Puede autorizar una orden"),
            ("rechazar_orden", "Puede rechazar una orden"),
        )
