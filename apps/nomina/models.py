from django.db import models
import datetime
from ..employees_and_jobs.models import Employee
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Roster(models.Model):
    date = models.DateField(default=datetime.date.today)
    estado = models.BooleanField(default=True)

class EmployeeRoster(models.Model):
    roster = models.ForeignKey(Roster, on_delete=models.CASCADE)
    # Until merge Employees
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    gross_salary = models.FloatField(default=0.0)
    tax = models.FloatField(default=0.0)
    net_salary = models.FloatField(default=0.0)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return "%s %s" % (self.employee, self.date)


