from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView   

from .models import Cotizacion, SolicitudCompra, OrdenCompra
from .forms import OrdenCompraForm, SolicitudCompraForm, CotizacionForm
# Create your views here.


class Prueba(CreateView): ##esta sirve solo para hacer pruebas 
    model = Cotizacion
    form_class = CotizacionForm
    template_name= 'compras/prueba.html'
    success_url = '/admin'

class index(TemplateView):
    template_name= 'compras/index_compras.html'


######---CREATES---######
class CotizacionCreate(CreateView): 
    model = Cotizacion 
    form_class = CotizacionForm
    #template_name = 
    success_url = '/'   

class SolicitudCreate(CreateView): 
    model= SolicitudCompra
    form_class= SolicitudCompraForm
    #template_name= 
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
