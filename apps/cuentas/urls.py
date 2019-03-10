# Django

# Urls for the cuentas app

from django.urls import path
from apps.cuentas.views import *

urlpatterns = [
    path('', index, name='crearCuenta'),
    path('listarPagar/', listarPagar,  name='listarPagar'),
    path('listarCobrar/', listarCobrar, name='listarCobrar'),
    path('detalles/', listarDetalles, name='detalles'),
    path('createOrder/', createOrder, name='createOrder'),

    ]
