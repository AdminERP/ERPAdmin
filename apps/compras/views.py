from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.shortcuts import redirect  
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from easy_pdf.rendering import render_to_pdf


from .models import Cotizacion, SolicitudCompra, OrdenCompra
from .forms import OrdenCompraForm, SolicitudCompraForm, CotizacionForm
# Create your views here.

class index(LoginRequiredMixin,TemplateView):
    template_name= 'compras/index_compras.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = self.request.user
        context['usuario'] = usuario
        return context

######---CREATES---######
class SolicitudCreate(LoginRequiredMixin, CreateView): 
    model = SolicitudCompra
    form_class = SolicitudCompraForm
    template_name = 'compras/crear_solicitudes.html'
    success_url = reverse_lazy('compras:solicitudes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = self.request.user
        context['usuario'] = usuario
        return context

class CotizacionCreate(LoginRequiredMixin, CreateView):
    model = Cotizacion
    form_class = CotizacionForm
    template_name = 'compras/crear_cotizaciones.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = self.request.user
        solicitud = SolicitudCompra.objects.get(pk=self.kwargs['pk'])        
        context['solicitud'] = solicitud
        context['usuario'] = usuario
        return context

class OrdenCreate(LoginRequiredMixin, CreateView): 
    model = OrdenCompra
    form_class = OrdenCompraForm
    template_name = 'compras/crear_ordenes.html'
    success_url = reverse_lazy('compras:orden_listar')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = self.request.user
        cotizacion = Cotizacion.objects.get(pk=self.kwargs['pk'])
        context['cotizacion'] = cotizacion
        context['usuario'] = usuario
        return context

######---CONSULTAS---######
class SolicitudList(LoginRequiredMixin, ListView) : 
    model = SolicitudCompra
    template_name = 'compras/lista_solicitudes.html'
    def get_queryset(self):
        usuario = self.request.user
        queryset = SolicitudCompra.objects.filter(solicitante=usuario)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = self.request.user

        if usuario.cargo.name != "operario" and usuario.cargo.name != "gerente":
            #TODO: consultar los empleados a cargo para filtrar las solicitudes
            solicitudes_autorizar = SolicitudCompra.objects.filter(estado_aprobacion='pendiente')
            context['solicitudes_autorizar'] = solicitudes_autorizar

            if usuario.cargo.name == 'jefecompras':
                solicitudes_cotizar = SolicitudCompra.objects.filter(estado_aprobacion='aprobado_gerente')
                context['solicitudes_cotizar'] = solicitudes_cotizar

        elif usuario.cargo.name == "gerente":
            solicitudes_autorizar = SolicitudCompra.objects.filter(estado_aprobacion='aprobado_jefe')
            context['solicitudes_autorizar'] = solicitudes_autorizar

        context['usuario'] = usuario

        return context

class CotizacionList(LoginRequiredMixin, ListView) : 
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
        query_cotizaciones = Cotizacion.objects.filter(solicitud=solicitud)
        cotizaciones = []
        for cot in query_cotizaciones:
            cotizaciones.append(cot.id)
        orden = False
        try:
            ordenes = OrdenCompra.objects.filter(cotizacion_id__in=cotizaciones)
            if ordenes:
                orden = True
        except OrdenCompra.DoesNotExist:
            pass
        cantidad = query_cotizaciones.count()
        context['usuario'] = usuario
        context['solicitud'] = solicitud
        context['cantidad'] = cantidad
        context['orden'] = orden
        return context

class OrdenList(LoginRequiredMixin, ListView) : 
    model = OrdenCompra 
    template_name= 'compras/listar_ordenes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = self.request.user
        context['usuario'] = usuario
        return context
    
    def get_queryset(self):
        queryset = super(OrdenList, self).get_queryset()
        queryset = queryset.order_by('estado_aprobacion')
        return queryset


#######---UPDATES---#######
class SolicitudUpdate(LoginRequiredMixin, UpdateView): 
    model = SolicitudCompra
    form_class = SolicitudCompraForm
    template_name = "compras/crear_solicitudes.html"
    success_url = reverse_lazy('compras:solicitudes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = self.request.user
        context['usuario'] = usuario
        return context

@permission_required('compras.autorizar_solicitud')
def autorizarSolicitud(request, pk):
    solicitud = SolicitudCompra.objects.get(pk=pk)

    if solicitud.estado_aprobacion == 'pendiente':
        solicitud.estado_aprobacion = 'aprobado_jefe'
    elif solicitud.estado_aprobacion == 'aprobado_jefe':
        solicitud.estado_aprobacion = 'aprobado_gerente'

    solicitud.save()
    return redirect('compras:solicitudes')

@permission_required('compras.rechazar_solicitud')
def rechazarSolicitud(request, pk):
    solicitud = SolicitudCompra.objects.get(pk=pk)
    solicitud.estado_aprobacion = 'rechazada'
    solicitud.save()
    return redirect('compras:solicitudes')

@permission_required('compras.autorizar_orden')
def autorizarOrden(request, pk):
    orden = OrdenCompra.objects.get(pk=pk)
    orden.estado_aprobacion = 'aprobado_gerente'
    orden.save()
    send_aprov_notification(orden) 
    return redirect('compras:orden_listar')

@permission_required('compras.rechazar_orden')
def rechazarOrden(request, pk):
    orden = OrdenCompra.objects.get(pk=pk)
    orden.estado_aprobacion = 'rechazada'
    orden.save()
    send_reject_notification()
    return redirect('compras:orden_listar')

def send_aprov_notification(orden):
        #cuenta: servicioalcliente.compraserp@gmail.com
        #pass: compras123
        # TODO generar pdf con la informacion de la orden y considerar proveedor como dato maestro
        email = EmailMessage( 
            subject = 'Aprobación de Compra',
            body = 'Su cotización fue seleccionada y aprobada para compra. \n\n\n Gracias por sus servicios',
            from_email = settings.EMAIL_HOST_USER,
            to = ['daniel.bueno@correounivalle.edu.co', orden.cotizacion.proveedor.email ],
        )
        send_pdf = render_to_pdf(
        'compras/send.html',
        {'cotizacion': orden.cotizacion,},
        )
        email.attach('cotización.pdf', send_pdf , 'application/pdf')
        email.send()

# TODO enviar correo al solicitante y al jefe de compras informando que se rechazo
def send_reject_notification(): 
    pass


def create_pdf(): 
    return render_to_pdf(
        'compras/send.html',
        {'any_context_item_to_pass_to_the_template': context_value,},
)
...
    #.attach('file.pdf', post_pdf, 'application/pdf')

######---DELETES---######

class SolicitudDelete(LoginRequiredMixin, DeleteView):
    model = SolicitudCompra
    template_name = "compras/eliminar_solicitud.html"
    success_url = reverse_lazy('compras:solicitudes')

