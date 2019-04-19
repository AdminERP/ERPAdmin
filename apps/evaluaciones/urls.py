from os import name

from django.urls import path
from .views import *
from django.conf.urls import include, url

app_name = 'evaluaciones'

urlpatterns = [
    path('', inicio, name='inicio'),
    path('registrar-pregunta', registrar_pregunta, name='registrar_pregunta'),
    path('consultar-pregunta', consultar_pregunta, name='consultar_pregunta'),
    path('modificar-pregunta/<int:id>', registrar_pregunta, name='modificar_pregunta'),
    path('activar-pregunta/<int:id>', activar_pregunta, name='activar_pregunta'),
    path('desactivar-pregunta/<int:id>', desactivar_pregunta, name='desactivar_pregunta'),
    path('crear-evaluacion/<int:id>', creacion_evaluacion, name='crear_evaluacion'),
    path('registrar-evaluacion/<int:id>', registrar_evaluacion, name='registrar_evaluacion'),
    path('consultar-evaluacion', consultar_evaluacion, name='consultar_evaluacion'),
    path('modificar-evaluacion/<int:id>', registrar_evaluacion, name='modificar_evaluacion'),
    path('activar-evaluacion/<int:id>', activar_evaluacion, name='activar_evaluacion'),
    path('desactivar-evaluacion/<int:id>', desactivar_evaluacion, name='desactivar_evaluacion'),


]
