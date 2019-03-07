""" Modelos propios modulo Compras """

from django.db import models

# from usuarios import User

class Articulo(models.Model):
    # ¿realmente es necesario una entidad articulo?
    nombre = models.CharField(max_length=50)
    

class SolicitudCompra(models.Model):
    
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    justificacion = models.CharField(max_length=1000)
    fecha_realizada = models.DateField(auto_now_add=True)
    fecha_esperada = models.DateField()
    # solicitante = models.ForeignKey(User, null=True)
    aprobacion_departamento = models.BooleanField(default=False)
    # jefe_aprobo = models.ForeignKey(User, null=True)
    aprobacion_gerencia = models.BooleanField(default=False)
    # gerente_aprobo = models.ForeignKey(User, null=True)
    
    
class Proveedor(models.Model):
    
    nombre = models.CharField(max_length=50)
    email = models.EmailField()
    
class Cotizacion(models.Model):
    
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    cantidad = models.SmallIntegerField()

    fecha_realizada = models.DateField(auto_now_add=True)
    fecha_esperada = models.DateField()

    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)

class OrdenCompra(models.Model):

    cotizacion = models.ForeignKey(Cotizacion, on_delete=models.CASCADE)

    fecha_realizada = models.DateField(auto_now_add=True)
    #fecha_esperada = models.DateField()

    aprobacion_gerencia = models.BooleanField(default=False)
    # gerente_aprobo = models.ForeignKey(User, null=True)