from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView, View
from django.shortcuts import redirect  
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.core.mail import  EmailMessage
from django.conf import settings
from easy_pdf.rendering import render_to_pdf
from apps.datosmaestros.models import ValorModel
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from io import BytesIO
from xhtml2pdf import pisa
from apps.datosmaestros.models import ValorModel
from apps.usuarios.models import Usuario
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
            subordinados = []
            sub_query = Usuario.consultar_subordinados(usuario.id)
            for sub in sub_query:
                subordinados.append(sub.id)

            solicitudes_autorizar = SolicitudCompra.objects.filter(estado_aprobacion='pendiente', solicitante_id__in=subordinados)
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
    send_reject_notification(solicitud)
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
    send_reject_notification(orden.cotizacion.solicitud)
    return redirect('compras:orden_listar')

def send_aprov_notification(orden):
        #cuenta: servicioalcliente.compraserp@gmail.com
        #pass: compras123
        # TODO generar pdf con la informacion de la orden

        dato = orden.cotizacion.proveedor 
        valor_email_proveedor = ValorModel.objects.filter(dato=dato , nombre = 'email').get().valor

        email_proveedor = EmailMessage( 
            subject = 'Aprobación de Compra',
            body = 'Su cotización fue seleccionada y aprobada para compra. \n\n\n Gracias por sus servicios',
            from_email = settings.EMAIL_HOST_USER,
            to = [valor_email_proveedor,  ],
        )

        send_pdf = create_pdf(orden.cotizacion)
        email_proveedor.attach('cotización.pdf', send_pdf , 'application/pdf')
        email_proveedor.send()

        email_solicitante = EmailMessage(
            subject = 'Aprobación de Compra',
            body = 'Su solicitud de compra fue aprobada bajo la cotización adjunta.',
            from_email = settings.EMAIL_HOST_USER,
            to = [orden.cotizacion.solicitud.solicitante.email, ],
        )
        email_solicitante.attach('cotizacion', send_pdf, 'application/pdf')
        email_solicitante.send()


# TODO Adjuntar información de la solicitud
def send_reject_notification(solicitud): 
    email = EmailMessage( 
        subject = 'Aprobación de Compra',
        body = 'Su solicitud de compra no fue aprobada. ',
        from_email = settings.EMAIL_HOST_USER,
        to = [solicitud.solicitante.email, 
                solicitud.solicitante.jefe.email, ],
    )
    email.send()


def create_pdf(dato): 
    from django.utils import timezone

    context = {
        'date': timezone.now(),
        'dato': dato,
        'test': 'hola'

    }
    return render_to_pdf(
        'compras/send.html',
        {'context': context},
)



def render_pdf(url_template, context={}):
    ##Renderiza un template Django a un documento PDF

    template = get_template(url_template)
    html =template.render(context)
    result = BytesIO()
    pdf= pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result) 
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type = "application/pdf")
    return none

class PdfPrueba(View): 
    
    def get (self, request, *args, **kwargs): 
        pdf = render_pdf('compras/send.html')
        return HttpResponse(pdf, content_type='application/pdf')

######---DELETES---######

class SolicitudDelete(LoginRequiredMixin, DeleteView):
    model = SolicitudCompra
    template_name = "compras/eliminar_solicitud.html"
    success_url = reverse_lazy('compras:solicitudes')

