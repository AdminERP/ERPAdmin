from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from apps.prueba2.forms import RegistrarCargoForm
from apps.prueba2.forms import RegisterEmployeeForm
from apps.prueba2.models import Job
from apps.prueba2.models import Employee

def inicio(request):
    return render(request, 'base.html', {})


def registrar_cargo(request, id=None):
    cargo = None
    if id:
        cargo = get_object_or_404(Job, id=id)

    form = RegistrarCargoForm(instance=cargo)

    if request.method == "POST":
        form = RegistrarCargoForm(request.POST, instance=cargo)
        if form.is_valid():
            form.save()
            messages.success(request, "El cargo ha sido guardado correctamente.")
            return redirect('consultar_cargo')
        else:
            messages.error(request, 'Por favor verificar los campos en rojo.')
    return render(request, 'registrar_cargo.html', {'form': form})


def consultar_cargo(request):
    return render(request, 'consulta_cargos.html', {'lista_cargos': Job.objects.all()})


def desactivar_cargo(request, id):
    cargo = get_object_or_404(Job, id=id)
    cargo.estado = False
    cargo.save()
    messages.success(request, "El cargo ha sido desactivado correctamente del sistema")
    return redirect('consultar_cargo')


def activar_cargo(request, id):
    cargo = get_object_or_404(Job, id=id)
    cargo.estado = True
    cargo.save()
    messages.success(request, "El cargo ha sido activado correctamente en el sistema")
    return redirect('consultar_cargo')


def register_employee(request, id=None):
    employee = None
    if id:
        employee = get_object_or_404(Employee, id=id)

    form = RegisterEmployeeForm(instance=employee)

    if request.method == "POST":

        form = RegisterEmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, "El empleado ha sido guardado correctamente.")
            return redirect('consultar_empleado')
        else:
            messages.error(request, 'Por favor verificar los campos en rojo.')

        print(form.errors)
    return render(request, 'register_employee.html', {'form': form})


def consultar_empleado(request):
    return render(request, 'consulta_empleados.html', {'lista_empleados': Employee.objects.all(), 'action': 'list'})


def desactivar_empleado(request, id):
    empleado = get_object_or_404(Employee, id=id)
    empleado.status = False
    empleado.save()
    messages.success(request, "El empleado ha sido desactivado correctamente del sistema")
    return redirect('consultar_empleado')


def activar_empleado(request, id):
    empleado = get_object_or_404(Employee, id=id)
    empleado.status = True
    empleado.save()
    messages.success(request, "El empleado ha sido activado correctamente en el sistema")
    return redirect('consultar_empleado')