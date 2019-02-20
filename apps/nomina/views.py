from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from apps.employees_and_jobs.forms import RegistrarCargoForm
from apps.employees_and_jobs.forms import RegisterEmployeeForm
from apps.employees_and_jobs.models import Job, Employee
from apps.nomina.models import EmployeeRoster

from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
def inicio(request):
    return render(request, 'base.html', {})

def modulo_nomina(request, id=None):

    #employeeRoster = get_object_or_404(EmployeeRoster, id=id)
    return render(request, 'consulta_empleados.html', {'lista_empleados': Employee.objects.all(), 'action': 'roster'})

    '''
    if request.method == "POST":
        formset = question_formset(request.POST, queryset=preguntas_evaluacion)
        if formset.is_valid():
            formset.save()
            messages.success(request, "La nomina ha sido registrada correctamente para cada colaborador.")
            return redirect('consultar_evaluacion')
        else:
            messages.error(request, 'Por favor verificar los campos en rojo.')
    else:
        formset = question_formset(queryset=preguntas_evaluacion)
    return render(request, 'registrar_evaluaciones.html', {'evaluacion':evaluacion, 'formset': formset, 'preguntas': preguntas_evaluacion})
    '''

def creacion_nomina(request):
    print("hola")
    active_employees = Employee.objects.filter(status=True)
    for employee in active_employees:
        email(employee.salary, employee.email)
    return render(request, 'consulta_empleados.html', {'lista_empleados': Employee.objects.all(), 'action': 'roster'})




    '''
    employee = get_object_or_404(Employee, id=id)
    evaluacion = EmployeeEvaluation.objects.create(date=datetime.date.today(),
                                                   employee=employee)
    for pregunta in Question.objects.filter(estado=True):
        EmployeeEvaluationQuestions.objects.create(employeeEvaluationId=evaluacion, questionId=pregunta, score=0,
                                                   observation='')
    return redirect('registrar_evaluacion', evaluacion.id)
    '''

def pay_roster(request, id=None):
    #CREATE ROSTER OBJECTS AND SABE IN DATABASE
    return redirect('consultar_empleado')

def email(pay, email_to):
    subject = 'ERP ADMIN NOMINA'
    message = 'Se le ha cancelado ' + str(pay)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email_to]
    send_mail( subject, message, email_from, recipient_list )


