from django.shortcuts import render
from apps.inventario.models import *

# Create your views here.


def index (request):
    ordenes = OrdenCompra.listar()

    return render(request, 'inventario/entrada.html', {'ordenes':ordenes})
