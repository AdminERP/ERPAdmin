from django.urls import path
from apps.ordenes_servicio.views import *

app_name = 'ordenes_servicio'

urlpatterns = [
    path('crear-orden-servicio', crear_orden_servicio, name='crear_orden_servicio'),
    path('operadores-autocomplete', operadores_autocomplete, name='operadores_autocomplete'),
]