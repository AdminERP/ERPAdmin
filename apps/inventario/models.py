from django.db import models
#from apps.compras.models import OrdenCompra

from django.apps import apps


# Create your models here.

CONDICIONES = (
    (True, 'Buena'),
    (False, 'Mala')
)



class Entrada(models.Model):
    condicion = models.BooleanField(choices = CONDICIONES, default = 'Buena', null=False)
    comentario = models.CharField(max_length=500, null=True)
    fecha = models.DateField(auto_now_add = True)
    ordenCompra = models.ForeignKey('compras.OrdenCompra', null=False, blank=False, on_delete=models.CASCADE)

class Inventario(models.Model):
    articulo = models.CharField(max_length=100)
    cantidad = models.PositiveSmallIntegerField(null=True)
    entrada = models.ForeignKey(Entrada, null=False, blank=False, on_delete=models.CASCADE)
    estado = models.BooleanField(default = True)

    def __str__(self):
        return self.articulo

    @staticmethod
    def listar():
        try:
            salidas = Salida.objects.all()
            listaSalidas = []
            for salida in salidas:
                listaSalidas.append(salida.entrada.id)
            inventario = Inventario.objects.exclude(id__in=listaSalidas).filter(estado = True)
            return inventario
        except Inventario.DoesNotExist:
            return None

    @staticmethod
    def listarSalidas():
        try:
            salidas = Salida.objects.all()
            listaSalidas = []
            for salida in salidas:
                listaSalidas.append(salida.entrada.id)
            inventario = Inventario.objects.filter(id__in=listaSalidas, estado = True)
            return inventario
        except Inventario.DoesNotExist:
            return None

class Salida(models.Model):
    fecha = models.DateField(auto_now_add=True)
    entrada = models.ForeignKey(Inventario, null=False, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.articulo