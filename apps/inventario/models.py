from django.db import models

# Create your models here.

class OrdenCompra(models.Model):
    articulo = models.CharField(max_length=100)
    precio = models.CharField(max_length=100)
    cantidad = models.CharField(max_length=100)
    proveedores = models.CharField(max_length=100)
    total = models.CharField(max_length=100)
    tiempo = models.CharField(max_length=100)

    def __str__(self):
        return self.articulo

    @staticmethod
    def listar():
        try:
            ordenes = OrdenCompra.objects.all()
            return ordenes
        except OrdenCompra.DoesNotExist:
            return None

class Entrada(models.Model):
    condicion = models.BooleanField(default= True, null=False)
    razon_devolucion = models.CharField(max_length=500)
    fecha = models.DateField()
    ordenCompra = models.ForeignKey(OrdenCompra, null=False, blank=False, on_delete=models.CASCADE)



