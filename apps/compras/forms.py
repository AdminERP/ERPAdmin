from django import forms
from django.utils.translation import gettext as _
from django_select2.forms import Select2Widget

from .models import Cotizacion, SolicitudCompra, OrdenCompra
from apps.datosmaestros.models import DatoModel, CategoriaModel


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
            'cantidad' : forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la cantidad de articulos a solicitar'}),
            'articulo' : Select2Widget(),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categoria = CategoriaModel.objects.get(nombre="Articulos")
        self.fields['articulo'].queryset = DatoModel.objects.filter(categoria=categoria)


class CotizacionForm(forms.ModelForm):
    class Meta:
        model = Cotizacion

        fields = [
            'proveedor',
            'solicitud',
            'fecha_realizada',
            'total',
        ]

        labels = {
            'proveedor' : 'Proveedor',
            'fecha_realizada' : 'Fecha de realizacion de la cotizacion ',
            'solicitud' : 'Solicitud',
        }

        widgets = {
            'fecha_realizada' : forms.SelectDateWidget(empty_label = EMPTY_LABEL, months = MESES),
            'proveedor' : Select2Widget(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categoria = CategoriaModel.objects.get(nombre="Proveedores")
        self.fields['proveedor'].queryset = DatoModel.objects.filter(categoria=categoria)



class OrdenCompraForm(forms.ModelForm):
    class Meta:

        model = OrdenCompra

        fields = [
            'cotizacion',
            'fecha_esperada',
        ]

        labels = {
            'cotizacion' : 'Cotización ',
            'fecha_esperada' : 'Fecha esperada de entrega del producto',
        }

        widgets = {
            'cotizacion' : Select2Widget(),
            'fecha_esperada' : forms.SelectDateWidget(empty_label= EMPTY_LABEL, months = MESES) ,
        }
