# Django
from django.urls import path

# Datos Maestros views
from .views import index

app_name = 'datosmaestros'

urlpatterns = [
    path('', index, name = 'index'),
]
