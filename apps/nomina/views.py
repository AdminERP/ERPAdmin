from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from apps.employees_and_jobs.models import Job, Employee
from apps.nomina.models import EmployeePayroll, Payroll

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings

# Create your views here.
def inicio(request):
    return render(request, 'base.html', {})

def payroll_module(request, id=None):
    return render(request, 'consulta_empleados.html', {'lista_empleados': Employee.objects.all(), 'action': 'payroll'})



def create_payroll(request):
    active_employees = Employee.objects.filter(status=True)
    payroll_registry = Payroll.objects.create()
    payroll_registry.save()
    sum_payroll = 0
    total_error_not_payment = 0
    for employee in active_employees:
        try:
            email_to, gross_salary, tax, net_salary = register_payroll_individual(employee, payroll_registry)
        except:
            print("Hubo un error con registro de nomina de " + employee.name)
            total_error_not_payment = total_error_not_payment + 1
        else:
            try:
                email(email_to=email_to, name=employee.name, id_type=employee.id_type, id_number=employee.identification,
                      gross_salary=gross_salary, tax=tax, net_salary=net_salary, bank=employee.bank, eps=employee.eps,
                      pension_fund=employee.pension_fund, severance_fund=employee.severance_fund,
                      date_payment=payroll_registry.date)
                sum_payroll = sum_payroll + employee.salary
            except OSError as e:
                print("Hubo un error al conectar con la red para enviar correo")
                total_error_not_payment = total_error_not_payment + 1

    if total_error_not_payment == 0:
        send_data = {
            'message': "La nomina ha sido registrada correctamente para cada colaborador.",
            'type': 'success'
        }
    else:
        send_data = {
            'message': "Hubo un error al enviar "+ str(total_error_not_payment) + " de " + str(len(active_employees)),
            'type': 'error'
        }

    return JsonResponse(send_data)


def register_payroll_individual(employee,payroll_registry):
    tax_calculation = employee.salary * 0.3
    net_salary = employee.salary - tax_calculation
    employee_payroll = EmployeePayroll.objects.create(payroll=payroll_registry, employee=employee,
                                                    gross_salary=employee.salary, tax=tax_calculation,
                                                    net_salary=net_salary)
    #employee_payroll.save()
    return employee.email, employee_payroll.gross_salary, employee_payroll.tax, employee_payroll.net_salary


def deactivate_payroll(request, id):
    employee_payroll = get_object_or_404(EmployeePayroll, id=id)
    employee_payroll.estado = False
    employee_payroll.save()
    messages.success(request, "La nomina del empleado ha sido desactivada correctamente del sistema")
    return redirect('consultar_nomina')


def activate_payroll(request, id):
    employee_payroll = get_object_or_404(EmployeePayroll, id=id)
    employee_payroll.estado = True
    employee_payroll.save()
    messages.success(request, "La nomina del empleado ha sido activada correctamente en el sistema")
    return redirect('consultar_nomina')


def payroll_consult(request):
    return render(request, 'consult_payroll.html', {'lista_nomina': EmployeePayroll.objects.all()})


def email(email_to, name, id_type, id_number, gross_salary, tax, net_salary, bank, eps, pension_fund, severance_fund, date_payment):
    template_txt_file = get_template('payroll_email.txt')
    template_html = get_template('payroll_email.html')

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



