from os import name

from django.urls import path
from .views import *

urlpatterns = [
    path('', inicio, name='inicio'),
    path('modulo-nomina', roster_module, name='modulo_nomina'),
    path('creacion_nomina', create_roster, name='creacion_nomina'),



]