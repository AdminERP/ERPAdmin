from os import name

from django.urls import path
from .views import *

app_name = 'nomina'

urlpatterns = [
    path('', inicio, name='inicio'),
    path('modulo-nomina', payroll_module, name='modulo_nomina'),
    path('creacion_nomina', create_payroll, name='creacion_nomina'),
    path('consultar-nomina', payroll_consult, name='consultar_nomina'),
    path('activar-nomina/<int:id>', activate_payroll, name='activar_nomina'),
    path('desactivar-nomina/<int:id>', deactivate_payroll, name='desactivar_nomina')



]