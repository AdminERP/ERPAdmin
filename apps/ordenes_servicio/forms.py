from django import forms
from apps.ordenes_servicio.models import *

class OrdenServicioForm(forms.ModelForm):
    encargado_select = forms.CharField(label = "Encargado:",required=False, widget=forms.TextInput(
        attrs={
            'class': 'basicAutoSelect',
            'data-url': "operadores-autocomplete",
            'placeholder' : "Buscar un operario",
            "data-noresults-text" : "No hay resultados",
        }))
    class Meta:
        model = OrdenServicio
        fields = ('servicio_vendido', 'encargado', 'cliente', 'comentarios')