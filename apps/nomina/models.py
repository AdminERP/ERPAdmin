from django.db import models
import datetime
from ..usuarios.models import Usuario
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Payroll(models.Model):
    date = models.DateField(default=datetime.date.today)
    estado = models.BooleanField(default=True)

    class Meta:
        permissions = (
            ('view_payroll', 'Puede consultar las nominas que se han realizado'),
            ('activate_payroll', 'Puede activar/desactivar nominas ejecutadas'),
        )

class EmployeePayroll(models.Model):
    payroll = models.ForeignKey(Payroll, on_delete=models.CASCADE)
    # Until merge Employees
    employee = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    gross_salary = models.FloatField(default=0.0)
    tax = models.FloatField(default=0.0)
    net_salary = models.FloatField(default=0.0)
    estado = models.BooleanField(default=True)

    class Meta:
        permissions = (
            ('view_employeepayroll', 'Puede consultar las nominas de cada empleado'),
            ('activate_employeeepayroll', 'Puede activar/desactivar nominas de cada empleado'),
        )

    def __str__(self):
        return "%s %s" % (self.employee, self.date)


