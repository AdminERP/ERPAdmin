from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from apps.prueba2.forms import RegistrarCargoForm
from apps.prueba2.models import Job


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
    messages.success("El cargo ha sido desactivado correctamente del sistema")
    return redirect("consultar_cargo")

def activar_cargo(request, id):
    cargo = get_object_or_404(Job, id=id)
    cargo.estado = True
    cargo.save()
    messages.success("El cargo ha sido activado correctamente en el sistema")
    return redirect("consultar_cargo")