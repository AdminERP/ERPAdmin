# Django

# Urls for the invetario app

from django.urls import path
from apps.inventario.views import *

urlpatterns = [
    path('', index, name='landingInventario'),
    path('entradas', entradas, name='entradas'),
    path('entradasRegistradas', entradasRegistradas, name='entradasRegistradas'),
    path('list', inventario, name= 'inventario'),
    path('crearEntrada/<str:idOrden>', registroEntrada, name= 'registroEntrada')

]
