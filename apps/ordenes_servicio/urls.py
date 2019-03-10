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
    path('operadores-autocomplete', operadores_autocomplete, name='operadores_autocomplete'),
    path('clientes-autocomplete', clientes_autocomplete, name='clientes_autocomplete'),
]