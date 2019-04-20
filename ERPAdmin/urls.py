from django.urls import path, include

urlpatterns = [
    path('', include('apps.usuarios.urls', namespace = 'usuarios')),
    path('datos-maestros/', include('apps.datosmaestros.urls', namespace = 'datosmaestros')),
    path('ordenes_servicio/',  include('apps.ordenes_servicio.urls')),
]