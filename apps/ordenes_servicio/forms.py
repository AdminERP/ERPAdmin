from django import forms
from apps.ordenes_servicio.models import *
from django.urls import reverse_lazy

class OrdenServicioForm(forms.ModelForm):
    encargado_select = forms.CharField(label = "Buscar Encargado:",required=False, widget=forms.TextInput(
        attrs={
            'class': 'basicAutoSelect',
            'data-url': reverse_lazy("ordenes_servicio:operadores_autocomplete"),
            'placeholder' : "Buscar un operario",
            "data-noresults-text" : "No hay resultados",
        }))
    encargado = forms.CharField(required=True)
    class Meta:
        model = OrdenServicio
        fields = ('servicio_vendido', 'cliente', 'comentarios')