""" Modelos propios modulo Compras """

from django.db import models


class Articulo(models.Model):
    
    nombre = models.CharField(max_length=50)
    

class SolicitudCompra(models.Model):
    
    articulos
    justificacion = models.CharField(max_length=1000)
    tiempo_esperado = models.SmallIntegerField()
    aprobacion_departamento = models.BooleanField()
    aprobacion_gerencia = models.BooleanField()
    
    
class Proveedor(models.Model):
    
    nombre = models.CharField(max_length=50)
    email = models.EmailField()
    
class Cotizacion(models.Model):


class OrdenCompra(models.Model):