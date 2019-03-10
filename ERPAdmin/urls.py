from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('datos-maestros/', include('apps.datosmaestros.urls', namespace = 'datosmaestros')),
]
