"""ERPAdmin Compras URL Configuration """

from django.urls import path
from django.views.generic.base import TemplateView

from .views import SolicitudList

urlpatterns = [
    path('',TemplateView.as_view(template_name='index_compras.html'), name='index'),
    # path('solicitud/crear', ,name='solicitud_crear'),
    path('solicitud/', SolicitudList.as_view(), name='solicitud'),
    path('solicitud/listar', SolicitudList.as_view(), name='solicitud_listar'),
    # path('solicitud/detalle/<int:pk>', ,name='solicitud_detalles'),
    # 
    # path('orden/crear', ,name='orden_crear'),
    # path('orden/listar', ,name='orden_listar'),
    # path('orden/detalle/<int:pk>', ,name='orden_detalle'),
]