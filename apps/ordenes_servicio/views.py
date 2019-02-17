from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import *
from django.db import models

#autocomplete
from apps.usuarios.models import User
from django.http import HttpResponseRedirect, JsonResponse

# Create your views here.

def crear_orden_servicio(request):
    # user = request.user
    # Validar que el usuario sea un coordinador de servicios
    if True:
        form = None
        if request.method == 'POST':
            form = OrdenServicioForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Orden de servicio creada exitosamente')
                form = OrdenServicioForm()
            else:
                messages.error(request, 'Por favor corrige los errores')
        else:
            form = OrdenServicioForm()
        return render(request, 'crear_orden_servicio.html', {'form': form})
    else:
        messages.error(request, 'No estas autorizado para realizar esta acción')
        return redirect('accounts:home')

def operadores_autocomplete(request):
    # user = request.user
    # Validar que el usuario sea un coordinador de servicios
    json = []
    if request.GET.get('q'):
        q = request.GET['q']
        data = User.objects.filter(models.Q(cedula__icontains=q) | models.Q(first_name__icontains=q) | models.Q(last_name__icontains=q)).values_list('cedula', 'first_name', 'last_name')[:10]
        arr = list(data)
        for tupla in arr:
            cedula = tupla[0]
            nombre = tupla[1]
            apellidos = tupla[2]
            json.append(cedula + ' - ' + nombre + ' ' + apellidos)
    return JsonResponse(json, safe=False)