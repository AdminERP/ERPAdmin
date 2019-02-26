from os import name

from django.urls import path
from .views import *

urlpatterns = [
    path('', inicio, name='inicio'),
    path('modulo-nomina', payroll_module, name='modulo_nomina'),
    path('creacion_nomina', create_payroll, name='creacion_nomina'),



]