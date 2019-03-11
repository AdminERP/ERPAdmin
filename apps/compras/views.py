from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.shortcuts import redirect  

from .models import Cotizacion, SolicitudCompra, OrdenCompra
from .forms import OrdenCompraForm, SolicitudCompraForm, CotizacionForm
# Create your views here.

#TODO: proteger vista con login
class index(TemplateView):
    template_name= 'compras/index_compras.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = self.request.user
        ###
        # Comentar todas las siguientes lineas excepto la del rol a probar
        usuario.rol = "operario"
        # usuario.rol = "jefe_compras"
        # usuario.rol = "gerente"
        ####
        context['usuario'] = usuario
        return context


######---CREATES---######
#TODO: proteger vista con login y rol diferente a gerente
class SolicitudCreate(CreateView): 
    model = SolicitudCompra
    form_class = SolicitudCompraForm
    template_name = 'compras/crear_solicitudes.html'
    success_url = reverse_lazy('compras:solicitudes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = self.request.user
        context['usuario'] = usuario
        return context

#TODO: proteger vista con login y solo rol jefe_compras    
class CotizacionCreate(CreateView): 
    model = Cotizacion 
    form_class = CotizacionForm
    #template_name = 
    success_url = '/'   

#TODO: proteger vista con login y solo rol jefe_compras    
class OrdenCreate(CreateView): 
    model = OrdenCompra
    form_class= OrdenCompraForm
    #template_name = 
    success_url= '/'


######---CONSULTAS---######
#TODO: proteger vista con login   
class SolicitudList(ListView) : 
    model = SolicitudCompra
    template_name = 'compras/lista_solicitudes.html'
    def get_queryset(self):
        usuario = self.request.user
        queryset = SolicitudCompra.objects.filter(solicitante=usuario)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = self.request.user
        ###
        # TODO: Se debe evaluar el rol segun lo establezca el grupo de roles y permisos
        # Mientras, comentar todas las siguientes lineas excepto la del rol a probar
        # usuario.rol = "operario"
        usuario.rol = "jefe_compras"
        # usuario.rol = "gerente"
        ####
        if usuario.rol != "operario" and usuario.rol != "gerente":
            #TODO: consultar los empleados a cargo para filtrar las solicitudes
            solicitudes_autorizar = SolicitudCompra.objects.filter(estado_aprobacion='pendiente')
            context['solicitudes_autorizar'] = solicitudes_autorizar

            if usuario.rol == 'jefe_compras':
                solicitudes_cotizar = SolicitudCompra.objects.filter(estado_aprobacion='aprobado_gerente')
                context['solicitudes_cotizar'] = solicitudes_cotizar

        elif usuario.rol == "gerente":
            solicitudes_autorizar = SolicitudCompra.objects.filter(estado_aprobacion='aprobado_jefe')
            context['solicitudes_autorizar'] = solicitudes_autorizar

        context['usuario'] = usuario

        return context

#TODO: proteger vista con login y rol jefe_compras
class CotizacionList(ListView) : 
    model = Cotizacion 
    template_name= 'compras/listar_cotizaciones.html'
    
    def get_queryset(self):
        solicitud = SolicitudCompra.objects.get(pk=self.kwargs['pk'])
        queryset = Cotizacion.objects.filter(solicitud=solicitud)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = self.request.user
        solicitud = SolicitudCompra.objects.get(pk=self.kwargs['pk'])
        usuario.rol = 'Jefe de Compras'
        context['usuario'] = usuario
        context['solicitud'] = solicitud
        return context

#TODO: proteger vista con login y rol jefe_compras o gerente   
class OrdenList(ListView) : 
    model = OrdenCompra 
    template_name= 'compras/prueba.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = self.request.user
        ###
        # Comentar todas las siguientes lineas excepto la del rol a probar
        usuario.rol = "jefe_compras"
        # usuario.rol = "gerente"
        ####
        context['usuario'] = usuario
        return context


#######---UPDATES---#######
#TODO: proteger vista con login
class SolicitudUpdate(UpdateView): 
    model = SolicitudCompra
    form_class = SolicitudCompraForm
    template_name = "compras/crear_solicitudes.html"
    success_url = reverse_lazy('compras:solicitudes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = self.request.user
        context['usuario'] = usuario
        return context

#TODO: proteger vista con login y rol jefe_compras
def autorizarSolicitud(request, pk):
    solicitud = SolicitudCompra.objects.get(pk=pk)

    if solicitud.estado_aprobacion == 'pendiente':
        solicitud.estado_aprobacion = 'aprobado_jefe'
    elif solicitud.estado_aprobacion == 'aprobado_jefe':
        solicitud.estado_aprobacion = 'aprobado_gerente'

    solicitud.save()
    return redirect('compras:solicitudes')

#TODO: proteger vista con login y rol jefe_compras
def rechazarSolicitud(request, pk):
    solicitud = SolicitudCompra.objects.get(pk=pk)
    solicitud.estado_aprobacion = 'rechazada'
    solicitud.save()
    return redirect('compras:solicitudes')

######---DELETES---######

class SolicitudDelete(DeleteView):
    model = SolicitudCompra
    template_name = "compras/eliminar_solicitud.html"
    success_url = reverse_lazy('compras:solicitudes')

