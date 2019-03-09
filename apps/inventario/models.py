from django.db import models

# Create your models here.

CONDICIONES = (
    (True, 'Buena'),
    (False, 'Mala')
)

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
    def listarAtendidas():
        try:
            entradas = Entrada.objects.all()
            listaOrdenes = []
            for entrada in entradas:
                listaOrdenes.append(entrada.ordenCompra.id)
            ordenes = OrdenCompra.objects.filter(id__in = listaOrdenes)
            return ordenes
        except OrdenCompra.DoesNotExist:
            return None

    @staticmethod
    def listarNoAtendidas():
        try:
            entradas = Entrada.objects.all()
            listaOrdenes = []
            for entrada in entradas:
                listaOrdenes.append(entrada.ordenCompra.id)
            ordenes = OrdenCompra.objects.exclude(id__in = listaOrdenes)
            return ordenes
        except OrdenCompra.DoesNotExist:
            return None

class Entrada(models.Model):
    condicion = models.BooleanField(choices = CONDICIONES, default = 'Buena', null=False)
    comentario = models.CharField(max_length=500, null=True)
    fecha = models.DateField(auto_now_add = True)
    ordenCompra = models.ForeignKey(OrdenCompra, null=False, blank=False, on_delete=models.CASCADE)

class Inventario(models.Model):
    articulo = models.CharField(max_length=100)
    cantidad = models.PositiveSmallIntegerField(null=True)
    entrada = models.ForeignKey(Entrada, null=False, blank=False, on_delete=models.CASCADE)
    #estado = models.BooleanField(default = True)

    def __str__(self):
        return self.articulo

    @staticmethod
    def listar():
        try:
            inventario = Inventario.objects.all()
            return inventario
        except Inventario.DoesNotExist:
            return None
