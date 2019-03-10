""" Modelos propios modulo Compras """

from django.db import models
#Se importa el User por defecto en espera de la implentacion del otro grupo
from django.contrib.auth.models import User as Usuario
# from apps.usuarios import Usuario

class Proveedor(models.Model):
    
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=50)
    telefono = models.CharField(max_length=10)
    email = models.EmailField()

class Articulo(models.Model):
    
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=150)
    

class SolicitudCompra(models.Model):
    
    PENDIENTE = 'pendiente'
    APROBADO_JEFE = 'aprobado_jefe'
    APROBADO_GERENTE = 'aprobado_gerente'

    ESTADOS = [
        (PENDIENTE, 'Pendiente aprobacion'),
        (APROBADO_JEFE, 'Aprobado jefe'),
        (APROBADO_GERENTE, 'Aprobado gerente')
    ]

    justificacion = models.CharField(max_length=1000)
    fecha_realizada = models.DateField(auto_now_add=True)
    fecha_esperada = models.DateField()
    
    estado_aprobacion = models.CharField(max_length=16, choices=ESTADOS, default=PENDIENTE)

    solicitante = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True)
    articulos = models.ManyToManyField(Articulo, through='ArticulosSolicitud')
    # Estos campos son verdaderamente necesarios?
    # jefe_aprobo = models.ForeignKey(Usuario, null=True)
    # gerente_aprobo = models.ForeignKey(Usuario, null=True)

class ArticulosSolicitud(models.Model):

    cantidad = models.SmallIntegerField()

    solicitud = models.ForeignKey(SolicitudCompra, on_delete=models.CASCADE)
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)


class Cotizacion(models.Model):
    
    total = precio = models.DecimalField(max_digits=17,decimal_places=2)    # Representa desde 0,00 hasta (10E15)-1,99 en pesos.
    fecha_realizada = models.DateField(auto_now_add=True)

    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    solicitud = models.ForeignKey(SolicitudCompra, on_delete=models.CASCADE)
    articulos = models.ManyToManyField(Articulo, through='ArticulosCotizacion')


class ArticulosCotizacion(models.Model):

    cotizacion = models.ForeignKey(Cotizacion, on_delete=models.CASCADE)
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)

    cantidad = models.SmallIntegerField()
    precio = models.DecimalField(max_digits=15,decimal_places=2)    # Representa desde 0,00 hasta (10E13)-1,99 en pesos.

class OrdenCompra(models.Model):

    PENDIENTE = 'pendiente'
    APROBADO_GERENTE = 'aprobado_gerente'
    EMITIDA = 'emitida_proveedor'

    ESTADOS = [
        (PENDIENTE, 'Pendiente aprobacion'),
        (APROBADO_GERENTE, 'Aprobado gerente'),
        (EMITIDA, 'Emitida al proveedor')
    ]
    # cotizaciones = models.ManyToManyField(Cotizacion)  # Al menos 3 por orden de compra, una sola elegida.
    cotizacion = models.ForeignKey(Cotizacion, on_delete=models.CASCADE)    # Elegida tambien puede definirse mediante flag en la relacion.

    fecha_realizada = models.DateField(auto_now_add=True)
    fecha_esperada = models.DateField()

    estado_aprobacion = models.CharField(max_length=16, choices=ESTADOS, default=PENDIENTE)
    # gerente_aprobo = models.ForeignKey(User, null=True)