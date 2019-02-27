from django.db import models

# Create your models here.
class CuentaEmpresa(models.Model):
    saldo = models.IntegerField()    


class CuentaPagar(models.Model):
    total = models.IntegerField()
    numero_orden = models.IntegerField()
    fecha_factura = models.DateTimeField()
    plazo = models.DateTimeField()
    estado = models.BooleanField()
    proveedor = models.CharField(max_length=30)
    cuenta_empresa = models.ForeignKey(CuentaEmpresa, on_delete=models.CASCADE)



class Item(models.Model):
    cuenta_por_pagar = models.ForeignKey(CuentaPagar, on_delete=models.CASCADE)
    detalle = models.CharField(max_length=30)
    precio_total = models.IntegerField()

class CuentaCobrar(models.Model):
    tarifa = models.IntegerField()
    costo_total = models.IntegerField()
    Fecha_vencimiento = models.DateTimeField()
    estado = models.BooleanField()
    servicio = models.CharField(max_length=50)
    cuenta_empresa = models.ForeignKey(CuentaEmpresa, on_delete=models.CASCADE)