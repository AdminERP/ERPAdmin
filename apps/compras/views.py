from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView   

from .models import Cotizacion, SolicitudCompra, OrdenCompra
from .forms import OrdenCompraForm, SolicitudCompraForm, CotizacionForm
# Create your views here.

class index(TemplateView):
    template_name= 'compras/index_compras.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = self.request.user
        ###
        # Comentar todas las siguientes lineas excepto la del rol a probar
        # usuario.rol = "operario"
        usuario.rol = "jefe_compras"
        # usuario.rol = "gerente"
        ####
        context['usuario'] = usuario
        return context


######---CREATES---######
class SolicitudCreate(CreateView): 
    model= SolicitudCompra
    form_class= SolicitudCompraForm
    template_name= 'compras/crear_solicitudes.html'
    success_url = reverse_lazy('compras:solicitudes')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = self.request.user
        ###
        # Se debe evaluar el rol segun lo establezca el grupo de roles y permisos
        # Mientras, comentar todas las siguientes lineas excepto la del rol a probar
        # usuario.rol = "operario"
        usuario.rol = "jefe_compras"
        # usuario.rol = "gerente"
        ####
        context['usuario'] = usuario

        return context

class CotizacionCreate(CreateView): 
    model = Cotizacion 
    form_class = CotizacionForm
    #template_name = 
    success_url = '/'   

class OrdenCreate(CreateView): 
    model = OrdenCompra
    form_class= OrdenCompraForm
    #template_name = 
    success_url= '/'


######---CONSULTAS---######
class CotizacionList(ListView) : 
    model = Cotizacion 
    template_name= 'compras/prueba.html'

class SolicitudList(ListView) : 
    model = SolicitudCompra 
    template_name= 'compras/lista_solicitudes.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = self.request.user
        ###
        # Se debe evaluar el rol segun lo establezca el grupo de roles y permisos
        # Mientras, comentar todas las siguientes lineas excepto la del rol a probar
        # usuario.rol = "operario"
        usuario.rol = "jefe_compras"
        # usuario.rol = "gerente"
        ####
        solicitudes_autorizar = []
        if usuario.rol == "jefe_compras" or usuario.rol == "gerente":
            #TODO: Consultar las solicitudes asociadas a sus empleados
            pass

        context['usuario'] = usuario
        context['solicitudes_autorizar'] = solicitudes_autorizar

        return context

class OrdenList(ListView) : 
    model = OrdenCompra 
    template_name= 'compras/prueba.html'


#######---UPDATES---#######
class CotizacionUpdate(UpdateView): 
    model = Cotizacion 
    form_class = CotizacionForm
    #template_name = 
    success_url = '/'   

class SolicitudUpdate(UpdateView): 
    model= SolicitudCompra
    form_class= SolicitudCompraForm
    #template_name= 
    success_url = '/'

class OrdenUpdate(UpdateView): 
    model = OrdenCompra
    form_class= OrdenCompraForm
    #template_name = 
    success_url= '/'


######---DELETES---######
class CotizacionDelete(DeleteView): 
    model = Cotizacion 
    #template_name 	= 
    success_url = '/'   

class SolicitudDelete(DeleteView): 
    model= SolicitudCompra
    #template_name= 
    success_url = '/'

class OrdenDelete(DeleteView): 
    model = OrdenCompra
    #template_name = 
    success_url= '/'
