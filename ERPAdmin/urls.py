from django.urls import path, include

urlpatterns = [
    path('', (include('apps.usuarios.urls', namespace='usuarios'))),
    path('', include('apps.evaluaciones.urls', namespace='evaluaciones')),
    path('', include('apps.nomina.urls', namespace='nomina')),
    path('datos-maestros/', include('apps.datosmaestros.urls', namespace = 'datosmaestros')),
]
