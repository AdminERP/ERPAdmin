"""ERPAdmin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cuentas/', include('apps.cuentas.urls'), name = 'cuentas'),
    path('', include('apps.usuarios.urls', namespace = 'usuarios')),
    path('datos-maestros/', include('apps.datosmaestros.urls', namespace = 'datosmaestros')),
    path('ordenes_servicio/',  include('apps.ordenes_servicio.urls')),
    path('inventario/',include('apps.inventario.urls'), name = 'inventario'),
    path('compras/', include(('apps.compras.urls', 'compras'), namespace='compras')),
    path('', include('apps.evaluaciones.urls', namespace='evaluaciones')),
    path('', include('apps.nomina.urls', namespace='nomina')),
]
