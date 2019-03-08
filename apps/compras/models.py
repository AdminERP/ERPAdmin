""" Modelos propios modulo Compras """

from django.db import models

# from usuarios import User

class Proveedor(models.Model):
    
    nombre = models.CharField(max_length=50)
    email = models.EmailField()

class Articulo(models.Model):
    
    nombre = models.CharField(max_length=50)
    
class ArticulosSolicitud(models.Model):

    cantidad = models.SmallIntegerField()

class ArticulosCotizacion(models.Model):

    cantidad = models.SmallIntegerField()
    precio = models.DecimalField(max_digits=15,decimal_places=2)    # Representa desde 0,00 hasta (10E13)-1,99 en pesos.

class SolicitudCompra(models.Model):
    
    PENDIENTE = 'pendiente'
    APROBADO_JEFE = 'aprobado_jefe'
    APROBADO_GERENTE = 'aprobado_gerente'

    ESTADOS = [
        (PENDIENTE, 'Pendiente aprobacion'),
        (APROBADO_JEFE, 'Aprobado jefe'),
        (APROBADO_GERENTE, 'Aprobado gerente')
    ]

    articulos = models.ManyToManyField(Articulo, through=ArticulosSolicitud)
    justificacion = models.CharField(max_length=1000)
    fecha_realizada = models.DateField(auto_now_add=True)
    fecha_esperada = models.DateField()
    # solicitante = models.ForeignKey(User, null=True)
    estado_aprobacion = models.CharField(max_length=16, choices=ESTADOS, default=PENDIENTE)
    # jefe_aprobo = models.ForeignKey(User, null=True)
    # gerente_aprobo = models.ForeignKey(User, null=True)
    
class Cotizacion(models.Model):
    
    articulos = models.ManyToManyField(Articulo, through=ArticulosCotizacion)
    cantidad = models.SmallIntegerField()
    total = precio = models.DecimalField(max_digits=17,decimal_places=2)    # Representa desde 0,00 hasta (10E15)-1,99 en pesos.

    fecha_realizada = models.DateField(auto_now_add=True)
    fecha_esperada = models.DateField()

    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)

class OrdenCompra(models.Model):

    PENDIENTE = 'pendiente'
    APROBADO_GERENTE = 'aprobado_gerente'
    EMITIDA = 'emitida_proveedor'

    ESTADOS = [
        (PENDIENTE, 'Pendiente aprobacion'),
        (APROBADO_GERENTE, 'Aprobado gerente'),
        (EMITIDA, 'Emitida al proveedor')
    ]

    cotizaciones = models.ManyToManyField(Cotizacion)  # Al menos 3 por orden de compra, una sola elegida.
    cotizacion_elegida = models.ForeignKey(Cotizacion, on_delete=models.CASCADE)    # Elegida tambien puede definirse mediante flag en la relacion.

    fecha_realizada = models.DateField(auto_now_add=True)
    fecha_esperada = models.DateField()

    estado_aprobacion = models.CharField(max_length=16, choices=ESTADOS, default=PENDIENTE)
    # gerente_aprobo = models.ForeignKey(User, null=True)