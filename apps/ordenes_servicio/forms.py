from django import forms
from apps.ordenes_servicio.models import *

class OrdenServicioForm(forms.ModelForm):
    class Meta:
        model = OrdenServicio
        fields = ('servicio_vendido', 'encargado', 'cliente', 'comentarios')