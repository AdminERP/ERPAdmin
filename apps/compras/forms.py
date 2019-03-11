from django import forms
from django.utils.translation import gettext as _
from django_select2.forms import Select2Widget

from .models import Cotizacion, SolicitudCompra, OrdenCompra



EMPTY_LABEL = ("Escoger Año", "Escoger Mes", "Escoger Día")
MESES = {
    1:_('ene'), 2:_('feb'), 3:_('mar'), 4:_('abr'),
    5:_('may'), 6:_('jun'), 7:_('jul'), 8:_('ago'),
    9:_('sep'), 10:_('oct'), 11:_('nov'), 12:_('dic')
}

class SolicitudCompraForm(forms.ModelForm):
    class Meta:
        model = SolicitudCompra

        fields = [
            'justificacion',
            'fecha_esperada',
            'estado_aprobacion',
            'articulo',
            'solicitante',
            'cantidad',
        ]
    
        labels = {
            'justificacion' : 'Justificación',
            'fecha_esperada' : 'Fecha esperada de entrega ',
            'estado_aprobacion' : 'Estado de aprobación',
            'articulo' : 'Articulo',
            'cantidad': 'Cantidad',
        }

        widgets = {
            'justificacion' : forms.TextInput(attrs = {'class': 'form-control'}),
            'fecha_esperada' : forms.SelectDateWidget(empty_label = EMPTY_LABEL, months = MESES) ,
            'estado_aprobacion' : Select2Widget(),
            'cantidad' : forms.NumberInput(attrs = {'class': 'form-control', 'placeholder': 'Ingrese la cantidad de articulos a solicitar'}),
            'articulo' : Select2Widget(),
        }


class CotizacionForm(forms.ModelForm):
    class Meta:
        model = Cotizacion

        fields = [ 
            'proveedor',
            'solicitud',
        ]

        labels = {
            'proveedor' : 'Proveedor',
            'solicitud' : 'Solicitud',
        }

        widgets = {
            'proveedor' : Select2Widget(),
            'solicitud' : Select2Widget(),
        }



class OrdenCompraForm(forms.ModelForm):
    class Meta:

        model = OrdenCompra

        fields = [
            'cotizacion',
            'estado_aprobacion',
            'fecha_esperada',
        ]

        labels = {
            'cotizacion' : 'Cotización ',
            'estado_aprobacion' :  'Aprobación de gerencia',
            'fecha_esperada' : 'Fecha esperada de entrega ',
        }

        widgets = {
            'cotizacion' : Select2Widget(),
            'estado_aprobacion' :  Select2Widget(),
            'fecha_esperada' : forms.SelectDateWidget(empty_label= EMPTY_LABEL, months = MESES) ,
        }
