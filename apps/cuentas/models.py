from django.db import models
from django.core.validators import MinValueValidator
from enum import Enum
from apps.compras.models import OrdenCompra
from apps.inventario.models import Entrada
from apps.datosmaestros.models import DatoModel
from apps.ordenes_servicio.models import OrdenServicio
# Create your models here.
class CuentaEmpresa(models.Model):
    saldo = models.DecimalField(null=False, validators=[MinValueValidator(0)], max_digits=10, decimal_places=2)   
    def __str__(self):
        return str(self.id)


class ServiceOrder(models.Model):
    status = models.CharField(max_length=254, null=False)
    sold_service = models.CharField(max_length=254, null=False)
    employee_id = models.IntegerField(null=False, validators=[MinValueValidator(1)])
    comments = models.TextField(max_length=508, null=True)
    total = models.DecimalField(null=False, validators=[MinValueValidator(0)], max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)

class CuentaPagar(models.Model):
    ORDER_STATUS = (
        ('1', 'Cancelled'),
        ('2', 'Paid'),
        ('3', 'Pending'),
        ('4', 'Overdue'),
    )
    
    total = models.DecimalField(null=False, validators=[MinValueValidator(0)], max_digits=10, decimal_places=2)
    invoice = models.CharField(max_length=255, null=False)
    invoice_date = models.DateField(null=False)
    term_date = models.DateField(null=False)
    status = models.CharField(max_length=1, choices=ORDER_STATUS)
    order = models.ForeignKey(OrdenCompra, null=False, blank=False, on_delete=models.CASCADE)
    supplier = models.ForeignKey(DatoModel, null=False, blank=False, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_id

    def to_dict_json(self):
        return {
            'pk':self.pk,
            'invoice_date':self.invoice_date,
            'term_date':self.term_date,
            'status':self.status,
            'order':self.order.id,
            'supplier_id':self.supplier_id,
            'total':self.total
        }
    @staticmethod
    def ordenesParaContabilizar():
        # return OrdenCompra.objects.all()
        try:
            entradas = Entrada.objects.all()
            if Entrada.DoesNotExist == True:
                return None
            else:
                entradas_orders_ids = []
                for entrada in entradas:
                    if entrada.condicion == True:
                        entradas_orders_ids.append(entrada.ordenCompra.id)
                orders = OrdenCompra.objects.filter(id__in=entradas_orders_ids)

                cuentas = CuentaPagar.objects.filter(status__in=[2,3,4])
                cuentas_orders_ids = []
                for cuenta in cuentas:
                    cuentas_orders_ids.append(cuenta.order.id)
                orders1 = orders.exclude(id__in=cuentas_orders_ids)
                return orders1
        except OrdenCompra.DoesNotExist:
            return None

    def db_table_exists(table_name):
        return table_name in connection.introspection.table_names()

    class Meta:
        permissions = (
            ('view_cuentaspagar', 'Puede ver las cuentas por pagar'),
            ('add_cuentaspagar', 'Puede agregar cuentas por pagar'),
            ('change_cuentaspagar', 'Puede actualizar cuentas por pagar'),
        )

class Item(models.Model):
    name = models.CharField(max_length=254, null=False)
    value = models.DecimalField(null=False, validators=[MinValueValidator(0)], max_digits=10, decimal_places=2)
    account = models.ForeignKey(CuentaPagar, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def uncommad(self):
        return str(self.value).replace(',', '.')

    class Meta:
        ordering = ('pk',)

class Payment(models.Model):
    account = models.ForeignKey(CuentaPagar, on_delete=models.CASCADE)
    #bank = models.ForeignKey(CuentaEmpresa, on_delete=models.CASCADE)
    bank = models.ForeignKey(DatoModel, null=False, blank=False, on_delete=models.CASCADE)
    total = models.DecimalField(null=False, validators=[MinValueValidator(0)], max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = (
            ('view_payments', 'Puede ver pagos'),
            ('add_payments', 'Puede agregar pagos'),
            ('change_payments', 'Puede actualizar pagos'),
        )

class CuentaCobrar(models.Model):
    tarifa = models.IntegerField(null=False, validators=[MinValueValidator(1)])
    costo_total = models.DecimalField(null=False, validators=[MinValueValidator(0)], max_digits=10, decimal_places=2)
    fecha_vencimiento = models.DateField(null=False)
    estado = models.BooleanField(True)
    servicio = models.CharField(max_length=254,null=False)
    cuenta_empresa = models.ForeignKey(DatoModel, on_delete=models.CASCADE, blank=False, null=False,
                                    limit_choices_to= {'categoria__nombre':"Bancos"},
                                    related_name='banco_set', verbose_name="Banco")
    service_order = models.ForeignKey(OrdenServicio, on_delete=models.CASCADE,null=True)

    class Meta:
        permissions = (
            ('view_cuentascobrar', 'Puede ver las cuentas por cobrar'),
            ('add_cuentascobrar', 'Puede agregar cuentas por cobrar'),
            ('change_cuentascobrar', 'Puede actualizar cuentas por cobrar'),
            ('view_ordenesservicio', 'Puede ver las ordenes de servicio en el area de cuentas'),
        )