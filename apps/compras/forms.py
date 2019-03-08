from django import forms
from apps.compras.models import Cotizacion, SolicitudCompra, OrdenCompra




EMPTY_LABEL=("Escoger Año", "Escoger Mes", "Escoger Día")
MESES = {
    1:_('ene'), 2:_('feb'), 3:_('mar'), 4:_('abr'),
    5:_('may'), 6:_('jun'), 7:_('jul'), 8:_('ago'),
    9:_('sep'), 10:_('oct'), 11:_('nov'), 12:_('dic')
}

class CotizacionForm(forms.ModelForm): 
    class Meta:
        model = Cotizacion

        fields= [ 
            'proveedor', 
            'articulo',
            'cantidad',
            'fecha_realizada',
            'fecha_esperada'
        ]

        labels = {
            'proveedor' : 'Proveedor',
            'articulo' : 'Artículo', 
            'cantidad' : 'Cantidad', 
            'fecha_realizada' : 'Fecha de realización', 
            'fecha_esperada' : 'Fecha esperada de entrega'
        }

        widgets = {
            'proveedor' : forms.Select(attrs= {'class': 'form-control'}) ,
            'articulo' :forms.Select(attrs= {'class': 'form-control'}) , 
            'cantidad' : forms.NumberInput(attrs= {'class': 'form-control'}) , 
            'fecha_realizada' : forms.DateField(widget=forms.SelectDateWidget(empty_label= EMPTY_LABEL,
                                                                                 months = MESES)) , 
            'fecha_esperada' : forms.DateField(widget=forms.SelectDateWidget(empty_label= EMPTY_LABEL,
                                                                                 months = MESES)) , 
        }



class SolicitudCompraForm (forms.ModelForm): 
    class Meta: 
        model = SolicitudCompra

        fields = [
            'articulo',
            'aprobacion_departamento',
            'aprobacion_gerencia',
            'justificacion',
            'fecha_realizada',
            'fecha_esperada',
            'aprobacion_departamento',
            'aprobacion_gerencia',
        ] 
        
        labels = {
            'articulo' : 'Artículo',
            'justificacion' : 'Justificación',
            'fecha_realizada' : 'Fecha de realización', 
            'fecha_esperada' : 'Fecha esperada de entrega ',
            'aprobacion_departamento' : 'Aprobación de departamento',
            'aprobacion_gerencia' : 'Aprobación de gerencia',
        }

        widgets = {
            'articulo' : forms.Select(attrs= {'class': 'form-control'}),
            'justificacion' : forms.TextInput(attrs= {'class': 'form-control'}),
            'fecha_realizada' :forms.DateField(widget=forms.SelectDateWidget(empty_label= EMPTY_LABEL,
                                                                                 months = MESES)) ,
            'fecha_esperada' :forms.DateField(widget=forms.SelectDateWidget(empty_label= EMPTY_LABEL,
                                                                                 months = MESES)) ,
            'aprobacion_departamento' :forms.CheckboxInput(attrs= {'class': 'form-control'}),
            'aprobacion_gerencia' : forms.CheckboxInput(attrs= {'class': 'form-control'})
        }


class OrdenCompraForm(forms.ModelForm): 
    class Meta: 

        model= OrdenCompra

        fields= [
            'cotizacion',
            'fecha_realizada',
            'aprobacion_gerencia',
        ]

        labels = {
            'cotizacion' : 'Cotización '
            'fecha_realizada' :  'Fecha de realización'
            'aprobacion_gerencia' :  'Aprobación de gerencia'
        }

        widgets = {
            'cotizacion' : forms.Select(attrs= {'class': 'form-control'}),
            'fecha_realizada' : forms.DateField(widget=forms.SelectDateWidget(empty_label= EMPTY_LABEL,
                                                                                 months = MESES))  ,
            'aprobacion_gerencia' :  forms.CheckboxInput(attrs= {'class': 'form-control'}),
        }