from django.db import models
import datetime
from ..prueba2.models import Job

# Create your models here.


class Question(models.Model):
    question_statement = models.CharField(max_length=2000)
    estado = models.BooleanField(default=True)
    def __str__(self):
        return self.name

class EmployeeEvaluation(models.Model):
    date = models.DateField(default=datetime.date.today)
    #Until merge Employees
    employee = models.ForeignKey(Job, on_delete=models.CASCADE)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class EmployeeEvaluationQuestions(models.Model):
    employeeEvaluation = models.ForeignKey(EmployeeEvaluation, on_delete=models.CASCADE)
    questionId = models.ForeignKey(Question, on_delete=models.CASCADE)
    observation = models.CharField(default='', max_length=2000)
    def __str__(self):
        return self.name