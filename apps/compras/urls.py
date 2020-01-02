"""ERPAdmin Compras URL Configuration """

from django.urls import path
from django.contrib.auth.decorators import permission_required

from .views import SolicitudList, index, SolicitudCreate, SolicitudUpdate, SolicitudDelete, autorizarSolicitud, rechazarSolicitud, CotizacionList, CotizacionCreate, OrdenCreate, OrdenList, autorizarOrden, rechazarOrden, PdfPrueba

urlpatterns = [
    path('', index.as_view(), name='index'),
    path('solicitud/crear', SolicitudCreate.as_view(), name='solicitud_crear'),
    path('solicitud/', SolicitudList.as_view(), name='solicitudes'),
    path('solicitud/listar', SolicitudList.as_view(), name='solicitudes_listar'),
    path('solicitud/editar/<int:pk>', SolicitudUpdate.as_view(), name='solicitud_edit'),
    path('solicitud/eliminar/<int:pk>', SolicitudDelete.as_view(), name='solicitud_delete'),
    path('solicitud/autorizar/<int:pk>', autorizarSolicitud, name='autorizar_solicitud'),
    path('solicitud/rechazar/<int:pk>', rechazarSolicitud, name='rechazar_solicitud'),
    path('cotizacion/listar/<int:pk>', permission_required('compras.view_cotizaciones')(CotizacionList.as_view()), name='cotizaciones_listar'),
    path('cotizacion/crear/<int:pk>', permission_required('compras.add_cotizacion')(CotizacionCreate.as_view()), name='cotizaciones_crear'),
    path('orden/crear/<int:pk>', permission_required('compras.add_cotizacion')(OrdenCreate.as_view()), name='orden_crear'),
    path('orden/listar', permission_required('compras.view_ordencompra')(OrdenList.as_view()), name='orden_listar'),
    path('orden/autorizar/<int:pk>', autorizarOrden, name='autorizar_orden'),
    path('orden/rechazar/<int:pk>', rechazarOrden, name='rechazar_orden'),
    path('cotizacion/send/', PdfPrueba.as_view() , name='sendpdf' ),
]
