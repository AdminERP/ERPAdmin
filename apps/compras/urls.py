"""ERPAdmin Compras URL Configuration """

from django.urls import path
from django.views.generic.base import TemplateView

urlpatterns = [
    path('',TemplateView.as_view(template_name='base.html'))
    # path('solicitud/crear', ,name='solicitud_crear'),
    # path('solicitud/listar', ,name='solicitud_listar'),
    # path('solicitud/detalle/<int:pk>', ,name='solicitud_detalles'),
    # 
    # path('orden/crear', ,name='orden_crear'),
    # path('orden/listar', ,name='orden_listar'),
    # path('orden/detalle/<int:pk>', ,name='orden_detalle'),
]