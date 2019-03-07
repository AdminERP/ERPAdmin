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
    def listar():
        try:
            ordenes = OrdenCompra.objects.all()
            #entradas = Entrada.objects.all()
            #listaOrdenes = []
            #for entrada in entradas:
            #    listaOrdenes.append(entrada.ordenCompra.id)

            #print(listaOrdenes)

            #for orden in listaOrdenes

            #print(entradas)
            return ordenes
        except OrdenCompra.DoesNotExist:
            return None

    @staticmethod
    def listarActivos():
        try:
            ordenes = OrdenCompra.objects.all()
            return ordenes
        except OrdenCompra.DoesNotExist:
            return None

class Entrada(models.Model):
    condicion = models.BooleanField(choices = CONDICIONES, default = 'Buena', null=False)
    razon_devolucion = models.CharField(max_length=500, null=True)
    fecha = models.DateField(auto_now = True)
    ordenCompra = models.ForeignKey(OrdenCompra, null=False, blank=False, on_delete=models.CASCADE)

class Inventario(models.Model):
    articulo = models.CharField(max_length=100)
    cantidad = models.PositiveSmallIntegerField(null=True)
    dependencia= models.CharField(max_length=100)
    entrada = models.ForeignKey(Entrada, null=False, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.articulo

    @staticmethod
    def listar():
        try:
            inventario = Inventario.objects.all()
            return inventario
        except Inventario.DoesNotExist:
            return None
