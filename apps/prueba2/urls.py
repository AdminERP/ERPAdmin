from os import name

from django.urls import path
from .views import *

urlpatterns = [
    path('', inicio, name='inicio'),
    path('registrar-cargo', registrar_cargo),
    path('consultar-cargo', consultar_cargo, name='consultar_cargo'),
    path('modificar-cargo/<int:id>', registrar_cargo, name='modificar_cargo'),
    path('activar-cargo/<int:id>', activar_cargo, name='activar_cargo'),
    path('desactivar-cargo/<int:id>', desactivar_cargo, name='desactivar_cargo'),


]