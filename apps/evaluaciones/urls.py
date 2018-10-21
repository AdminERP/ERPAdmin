from os import name

from django.urls import path
from .views import *

urlpatterns = [
    path('', inicio, name='inicio'),
    path('registrar-pregunta', registrar_pregunta),
    path('consultar-pregunta', consultar_pregunta, name='consultar_pregunta'),
    path('modificar-pregunta/<int:id>', registrar_pregunta, name='modificar_pregunta'),
    path('activar-pregunta/<int:id>', activar_pregunta, name='activar_pregunta'),
    path('desactivar-pregunta/<int:id>', desactivar_pregunta, name='desactivar_pregunta'),


]