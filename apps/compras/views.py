from django.shortcuts import render
from django.views.generic import ListView
from .models import SolicitudCompra

""" Views modulo Compras """

class ListarSolicitudes(ListView):
    model = SolicitudCompra
    template_name = "general.html"