from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.usuarios.urls', namespace = 'usuarios')),
    path('compras/', include(('apps.compras.urls', 'compras'), namespace='compras')),
    path('datos-maestros/', include('apps.datosmaestros.urls', namespace = 'datosmaestros')),
]
