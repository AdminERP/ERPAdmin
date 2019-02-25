from django.shortcuts import render
from apps.inventario.models import *

# Create your views here.


def index (request):

    return render(request, 'inventario/landing.html')

def entradas (request):
    ordenes = OrdenCompra.listar()

    return render(request, 'inventario/entrada.html', {'ordenes': ordenes})

def inventario (request):
    inventario = Inventario.listar()

    return render(request, 'inventario/inventario.html', {'inventario': inventario})