from django.urls import path
from apps.ordenes_servicio.views import *

app_name = 'ordenes_servicio'

urlpatterns = [
    path('',to_login,name="to_login"),
    path('login/', ordenes_login, name="Login"),
    path('logout/', gtfo, name="Logout"),
    path('welcome/', ordenes_welcome, name="Welcome"),
    path('crear_cliente/',crear_cliente,name="Crear Cliente"),
    path('consultar_clientes/',consultar_clientes,name="Consultar Clientes"),
    path('crear_orden_servicio/', crear_orden_servicio, name='crear_orden_servicio'),
    path('consultar_orden_servicio/', consultar_orden_servicio, name='consultar_orden_servicio'),
    path('cancelar_orden_servicio/<int:id>', cancelar_orden_servicio, name='cancelar_orden_servicio'),
    path('api/aceptar_orden_servicio/', aceptar_orden_servicio, name='aceptar_orden_servicio'),
    path('api/cerrar_orden_servicio/', cerrar_orden_servicio, name='cerrar_orden_servicio'),
    path('operadores-autocomplete', operadores_autocomplete, name='operadores_autocomplete'),
    path('clientes-autocomplete', clientes_autocomplete, name='clientes_autocomplete'),
]