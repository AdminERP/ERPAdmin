from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class CuentaEmpresa(models.Model):
    saldo = models.IntegerField()    


class CuentaPagar(models.Model):
    total = models.DecimalField(null=False, validators=[MinValueValidator(0)], max_digits=10, decimal_places=2)
    invoice_date = models.DateField(null=False)
    term_date = models.DateField(null=False)
    status = models.BooleanField(null=False)
    order_id = models.IntegerField(null=False, validators=[MinValueValidator(1)])
    supplier_id = models.IntegerField(null=False, validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Item(models.Model):
    name = models.CharField(max_length=254, null=False)
    value = models.DecimalField(null=False, validators=[MinValueValidator(0)], max_digits=10, decimal_places=2)
    account = models.ForeignKey(CuentaPagar, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CuentaCobrar(models.Model):
    tarifa = models.IntegerField()
    costo_total = models.IntegerField()
    Fecha_vencimiento = models.DateTimeField()
    estado = models.BooleanField()
    servicio = models.CharField(max_length=50)
    cuenta_empresa = models.ForeignKey(CuentaEmpresa, on_delete=models.CASCADE)