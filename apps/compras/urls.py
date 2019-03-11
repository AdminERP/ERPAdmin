"""ERPAdmin Compras URL Configuration """

from django.urls import path

from .views import SolicitudList, index, SolicitudCreate, SolicitudUpdate, SolicitudDelete

urlpatterns = [
    path('', index.as_view(), name='index'),
    path('solicitud/crear', SolicitudCreate.as_view(), name='solicitud_crear'),
    path('solicitud/', SolicitudList.as_view(), name='solicitudes'),
    path('solicitud/listar', SolicitudList.as_view(), name='solicitudes_listar'),
    path('solicitud/editar/<int:pk>', SolicitudUpdate.as_view() ,name='solicitud_edit'),
    path('solicitud/eliminar/<int:pk>', SolicitudDelete.as_view() ,name='solicitud_delete'),
    # path('orden/crear', ,name='orden_crear'),
    # path('orden/listar', ,name='orden_listar'),
    # path('orden/detalle/<int:pk>', ,name='orden_detalle'),
]
