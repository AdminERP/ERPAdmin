from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from apps.employees_and_jobs.models import Job, Employee
from apps.nomina.models import EmployeeRoster, Roster

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings

# Create your views here.
def inicio(request):
    return render(request, 'base.html', {})

def roster_module(request, id=None):
    return render(request, 'consulta_empleados.html', {'lista_empleados': Employee.objects.all(), 'action': 'roster'})



def create_roster(request):
    print("hola")
    active_employees = Employee.objects.filter(status=True)
    roster_registry = Roster.objects.create()
    roster_registry.save()
    sum_roster = 0
    total_error_not_payment = 0
    for employee in active_employees:
        try:
            email_to, gross_salary, tax, net_salary = register_roster_individual(employee, roster_registry)
        except:
            print("Hubo un error con registro de nomina de " + employee.name)
            total_error_not_payment = total_error_not_payment + 1
        else:
            email(email_to=email_to, name=employee.name, id_type=employee.id_type, id_number=employee.identification,
                  gross_salary=gross_salary, tax=tax, net_salary=net_salary, bank=employee.bank, eps=employee.eps,
                  pension_fund=employee.pension_fund, severance_fund=employee.severance_fund,
                  date_payment=roster_registry.date)
            sum_roster = sum_roster + employee.salary

    if total_error_not_payment == 0:
        messages.success(request, "La nomina ha sido registrada correctamente para cada colaborador.")
    else:
        messages.error(request, "Hubo un error al enviar "+ total_error_not_payment + "de " + str(len(active_employees)))

    return render(request, 'consulta_empleados.html', {'lista_empleados': Employee.objects.all(), 'action': 'roster'})


def register_roster_individual(employee,roster_registry):
    tax_calculation = employee.salary * 0.3
    net_salary = employee.salary - tax_calculation
    employee_roster = EmployeeRoster.objects.create(roster=roster_registry, employee=employee,
                                                    gross_salary=employee.salary, tax=tax_calculation,
                                                    net_salary=net_salary)
    #employee_roster.save()
    return employee.email, employee_roster.gross_salary, employee_roster.tax, employee_roster.net_salary



def email(email_to, name, id_type, id_number, gross_salary, tax, net_salary, bank, eps, pension_fund, severance_fund, date_payment):
    template_txt_file = get_template('roster_email.txt')
    template_html = get_template('roster_email.html')

    context_personal_employee_data = {'name': name,
         'id_type': id_type,
         'id_number': id_number,
         'gross_salary': gross_salary,
         'tax': tax,
         'net_salary': net_salary,
         'bank': bank,
         'eps': eps,
         'pension_fund': pension_fund,
         'severance_fund': severance_fund,
         'date_payment': date_payment,}

    subject, from_email = 'NOTIFICACIÓN DE LIQUIDACIÓN DE INGRESOS', settings.EMAIL_HOST_USER,
    text_content = template_txt_file.render(context_personal_employee_data)
    html_content = template_html.render(context_personal_employee_data)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [email_to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()



