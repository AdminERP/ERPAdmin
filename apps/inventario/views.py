from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.http.response import JsonResponse
from apps.inventario.models import *
from apps.inventario.forms import *

# Create your views here.

def index (request):
    return render(request, 'inventario/landing.html')

def entradas (request):
    ordenes = OrdenCompra.listarNoAtendidas()
    return render(request, 'inventario/entrada.html', {'ordenes': ordenes})

def entradasRegistradas (request):
    ordenes = OrdenCompra.listarAtendidas()
    ordenes = list(ordenes)
    listaEntradas = []
    for orden in ordenes:
        entrada = Entrada.objects.get(id = orden.id)
        listaEntradas.append(entrada)
    lista = zip(ordenes, listaEntradas)
    return render(request, 'inventario/entradasRegistradas.html', {'ordenes': lista})

def inventario (request):
    inventario = Inventario.listar()
    return render(request, 'inventario/inventario.html', {'inventario': inventario})

def registroEntrada(request, idOrden):
    orden = OrdenCompra.objects.get(id = idOrden)
    form = RegistroEntrada()

    if request.method == 'POST':
        form = RegistroEntrada(request.POST)

        if form.is_valid():
            nuevaEntrada = form.save()

            objeto = Inventario.objects.create(
            articulo = orden.articulo, cantidad = orden.cantidad, entrada = nuevaEntrada
            )
            objeto.save()

            messages.success(request, 'Entrada registrada exitosamente')
            return redirect('entradas')
        else:
            messages.error(request, 'Por favor corrige los errores')
            form = RegistroEntrada()
            return render(request, 'inventario/registrarEntrada.html', {'form': form, 'orden': orden})

    return render(request, 'inventario/registrarEntrada.html', {'form': form, 'orden': orden})

def salidas(request):
    salidas = Inventario.listarSalidas()
    return render(request, 'inventario/salidas.html', {'salidas' : salidas})

def salida(request):
    if request.is_ajax():
        id = request.POST.get('id', None)
        # Validar cuando un curso no exista.
        try:
            salida = Salida(entrada_id=id)
            salida.save()
            messages.success(request, 'Salida generada exitosamente')
        except Inventario.DoesNotExist as e:
            messages.error(request, 'El articulo no existe')
    else:
        messages.error(request, 'No estas autorizado para realizar esta acción')
    data = {'url': 'list'}
    return JsonResponse(data)