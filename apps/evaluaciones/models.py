from django.db import models
import datetime
from ..usuarios.models import Usuario
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class Question(models.Model):
    question_statement = models.CharField(max_length=2000)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.question_statement

    class Meta:
        permissions = (
            ('view_questions', 'Puede consultar las preguntas'),
            ('activate_question', 'Puede activar/desactivar preguntas'),
        )


class EmployeeEvaluation(models.Model):
    date = models.DateField(default=datetime.date.today)
    # Until merge Employees
    employee = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return "%s %s" % (self.employee, self.date)

    class Meta:
        permissions = (
            ('view_employeeevaluation', 'Puede consultar las evaluaciones de empleados'),
            ('activate_employeeevaluation', 'Puede activar/desactivar evaluaciones de empleados'),
        )


class EmployeeEvaluationQuestions(models.Model):
    employeeEvaluationId = models.ForeignKey(EmployeeEvaluation, on_delete=models.CASCADE,
                                             related_name='employee_evaluation_questions')
    questionId = models.ForeignKey(Question, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)],)
    observation = models.CharField(default='', max_length=2000)

    def __str__(self):
        return "%s %s %s %s" % (self.employeeEvaluationId, self.questionId, self.score, self.observation)

