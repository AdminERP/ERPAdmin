"""ERPAdmin Compras URL Configuration """

from django.urls import path
from django.views.generic.base import TemplateView

from .views import SolicitudList, index

urlpatterns = [
    path('', index.as_view(), name='index'),
    # path('solicitud/crear', ,name='solicitud_crear'),
    path('solicitud/', SolicitudList.as_view(), name='solicitudes'),
    path('solicitud/listar', SolicitudList.as_view(), name='solicitudes_listar'),
    # path('solicitud/detalle/<int:pk>', ,name='solicitud_detalles'),
    # 
    # path('orden/crear', ,name='orden_crear'),
    # path('orden/listar', ,name='orden_listar'),
    # path('orden/detalle/<int:pk>', ,name='orden_detalle'),
]