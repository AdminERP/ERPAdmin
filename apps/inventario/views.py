from django.shortcuts import render, redirect, reverse
from django.contrib import messages
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
        entrada = Entrada.objects.get(ordenCompra = orden)
        listaEntradas.append(entrada)
    lista = zip(ordenes, listaEntradas)
    return render(request, 'inventario/entradasRegistradas.html', {'ordenes': lista})

def editarEntrada(request, idEntrada, idOrden):
    entrada = Entrada.objects.get(id = idEntrada)
    form = RegistroEntrada (instance = entrada)
    if request.method == 'POST':
        form = RegistroEntrada(request.POST, instance = entrada)
        if form.is_valid():
            form.save()
            messages.success(request, 'Entrada registrada exitosamente')
            return redirect('entradasRegistradas')
        else:
            messages.error(request, 'Por favor corrige los errores')
    return render(request, 'inventario/editarEntrada.html', {'form': form, 'entrada': entrada, 'orden': idOrden})


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
