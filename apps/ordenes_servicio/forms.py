from django import forms
from apps.ordenes_servicio.models import *

class OrdenServicioForm(forms.ModelForm):
    encargado = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            'style': 'width: 400px',
            'class': 'basicAutoComplete',
            'data-url': "operadores-autocomplete"
        }))
    class Meta:
        model = OrdenServicio
        fields = ('servicio_vendido', 'cliente', 'comentarios')