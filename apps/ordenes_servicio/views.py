from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import *

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