from django.urls import path
from apps.ordenes_servicio.views import *

app_name = 'ordenes_servicio'

urlpatterns = [
    path('',to_welcome,name="to_welcome"),
    path('logout/', gtfo, name="Logout"),
    path('welcome/', ordenes_welcome, name="Welcome"),
    path('crear_orden_servicio/', crear_orden_servicio, name='crear_orden_servicio'),
    path('consultar_orden_servicio/', consultar_orden_servicio, name='consultar_orden_servicio'),
    path('api/cancelar_orden_servicio', cancelar_orden_servicio, name='cancelar_orden_servicio'),
    path('api/aceptar_orden_servicio/', aceptar_orden_servicio, name='aceptar_orden_servicio'),
    path('api/cerrar_orden_servicio/', cerrar_orden_servicio, name='cerrar_orden_servicio'),
    path('operadores-autocomplete', operadores_autocomplete, name='operadores_autocomplete'),
    path('clientes-autocomplete', clientes_autocomplete, name='clientes_autocomplete'),
]