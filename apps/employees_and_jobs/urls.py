from os import name

from django.urls import path
from .views import *

app_name='employees_and_jobs'

urlpatterns = [
    path('', inicio, name='inicio'),
    path('registrar-cargo', registrar_cargo, name='registrar_cargo'),
    path('consultar-cargo', consultar_cargo, name='consultar_cargo'),
    path('modificar-cargo/<int:id>', registrar_cargo, name='modificar_cargo'),
    path('activar-cargo/<int:id>', activar_cargo, name='activar_cargo'),
    path('desactivar-cargo/<int:id>', desactivar_cargo, name='desactivar_cargo'),
    path('registrar-empleado', register_employee, name='registrar_empleado'),
    path('consultar-empleado', consultar_empleado, name='consultar_empleado'),
    path('modificar-empleado/<int:id>', register_employee, name='modificar_empleado'),
    path('activar-empleado/<int:id>', activar_empleado, name='activar_empleado'),
    path('desactivar-empleado/<int:id>', desactivar_empleado, name='desactivar_empleado')

]