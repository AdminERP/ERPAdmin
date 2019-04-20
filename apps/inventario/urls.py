# Django

# Urls for the invetario app

from django.urls import path
from apps.inventario.views import *
app_name = 'inventario'
urlpatterns = [

    path('', index, name='landingInventario'),
    path('entradas', entradas, name='entradas'),
    path('entradasRegistradas', entradasRegistradas, name='entradasRegistradas'),
    path('list', inventario, name= 'inventario'),
    path('salidas', salidas, name= 'salidas'),
    path('salida', salida, name= 'salida'),
    path('crearEntrada/<str:idOrden>', registroEntrada, name= 'registroEntrada'),
    path('editarEntrada/<str:idEntrada>/<str:idOrden>/', editarEntrada, name= 'editarEntrada')

]
