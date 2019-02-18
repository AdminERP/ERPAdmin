from os import name

from django.urls import path
from .views import *

urlpatterns = [
    path('', inicio, name='inicio'),
    path('modulo-nomina', modulo_nomina, name='modulo_nomina'),
    path('pay_roster', pay_roster, name='pay_roster'),
    path('creacion_nomina', creacion_nomina, name='creacion_nomina'),



]