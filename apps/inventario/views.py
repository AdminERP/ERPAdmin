from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.http.response import JsonResponse
from apps.inventario.models import *
from apps.inventario.forms import *
from apps.compras.models import *
from django.contrib.auth.decorators import permission_required
from django.db import models

#Create your views here.
@permission_required('inventario.add_entrada', raise_exception=True)
def index (request):
    return render(request, 'usuarios/home.html')

@permission_required('inventario.add_entrada', raise_exception=True)
def entradas (request):

    ordenes = OrdenCompra.listarNoAtendidas()

    return render(request, 'entrada.html', {'ordenes': ordenes, })




@permission_required('inventario.change_entrada', raise_exception=True)
def entradasRegistradas (request):
    ordenes = OrdenCompra.listarAtendidas()
    ordenes = list(ordenes)
    listaEntradas = []
    for orden in ordenes:
        entrada = Entrada.objects.get(ordenCompra = orden)
        listaEntradas.append(entrada)
    lista = zip(ordenes, listaEntradas)
    return render(request, 'entradasRegistradas.html', {'ordenes': lista})

@permission_required('inventario.change_entrada', raise_exception=True)
def editarEntrada(request, idEntrada, idOrden):
    entrada = Entrada.objects.get(id = idEntrada)
    form = RegistroEntrada (instance = entrada)
    if request.method == 'POST':
        form = RegistroEntrada(request.POST, instance = entrada)
        if form.is_valid():
            data = form.save()

            if data.condicion:
                inventario = Inventario.objects.get(entrada_id=data.id)
                inventario.estado = True
                inventario.save()
            else:
                inventario = Inventario.objects.get(entrada_id=data.id)
                inventario.estado = False
                inventario.save()
            messages.success(request, 'Entrada registrada exitosamente')
            return redirect('inventario:entradasRegistradas')
        else:
            messages.error(request, 'Por favor corrige los errores')
    return render(request, 'editarEntrada.html', {'form': form, 'entrada': entrada, 'orden': idOrden})

@permission_required('inventario.add_salida', raise_exception=True)
def inventario (request):
    inventario = Inventario.listar()
    return render(request, 'bodega.html', {'inventario': inventario})

@permission_required('inventario.add_entrada', raise_exception=True)
def registroEntrada(request, idOrden):
    orden = OrdenCompra.objects.select_related('cotizacion').select_related('solicitud').get(id = idOrden)
    form = RegistroEntrada()

    if request.method == 'POST':
        form = RegistroEntrada(request.POST)

        if form.is_valid():
            nuevaEntrada = form.save()

            objeto = Inventario.objects.create(
            articulo = orden.solicitud.articulo.nombre, cantidad = orden.solicitud.cantidad, entrada = nuevaEntrada
            )
            objeto.save()

            messages.success(request, 'Entrada registrada exitosamente')
            return redirect('inventario:entradas')
        else:
            messages.error(request, 'Por favor corrige los errores')
            form = RegistroEntrada()
            return render(request, 'registrarEntrada.html', {'form': form, 'orden': orden})

    return render(request, 'registrarEntrada.html', {'form': form, 'orden': orden})

@permission_required('inventario.add_salida', raise_exception=True)
def salidas(request):
    salidas = Inventario.listarSalidas()
    return render(request, 'salidas.html', {'salidas' : salidas})

@permission_required('inventario.add_salida', raise_exception=True)
def salida(request):
    if request.is_ajax():
        id = request.POST.get('id', None)
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