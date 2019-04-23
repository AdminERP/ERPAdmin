from django import forms
from apps.ordenes_servicio.models import *
from django.urls import reverse_lazy

class CancelarOrdenServicioForm(forms.Form):
    comentario_cancelar = forms.CharField(label = "Comentarios sobre la cancelacion:",required=True)

class OrdenServicioForm(forms.ModelForm):
    encargado_select = forms.CharField(label = "Buscar Encargado:",required=False, widget=forms.TextInput(
        attrs={
            'class': 'basicAutoSelectEncargado',
            'data-url': reverse_lazy("ordenes_servicio:operadores_autocomplete"),
            'placeholder' : "Buscar un operario",
            "data-noresults-text" : "No hay resultados",
        }))
    encargado_seleccionado_texto = forms.CharField(label="Encargado:", required=False, widget=forms.TextInput(
        attrs={
            'placeholder' : "Encargado Seleccionado",
        }))
    cliente_select = forms.CharField(label = "Buscar Cliente:",required=False, widget=forms.TextInput(
        attrs={
            'class': 'basicAutoSelectCliente',
            'data-url': reverse_lazy("ordenes_servicio:clientes_autocomplete"),
            'placeholder' : "Buscar un cliente",
            "data-noresults-text" : "No hay resultados",
        }))
    cliente_seleccionado_texto = forms.CharField(label="Cliente:", required=False, widget=forms.TextInput(
        attrs={
            'placeholder' : "Cliente Seleccionado",
        }))
    class Meta:
        model = OrdenServicio
        fields = ('servicio_vendido', 'comentarios', 'cliente', 'encargado', 'fecha_atencion',)
        widgets = {
            'cliente': forms.HiddenInput(),
            'encargado': forms.HiddenInput(),
            'fecha_atencion':forms.TextInput(attrs={'type':'date'}),
            'comentarios':forms.Textarea(attrs={'placeholder':'Escriba un comentario'})
        }

    def clean(self):
        cleaned_data = self.cleaned_data
        cliente_aux = cleaned_data.get('cliente')
        encargado_aux = cleaned_data.get('encargado')
        if cliente_aux == None:
            msg = 'Debes seleccionar un Cliente'
            self._errors['cliente'] = self.error_class([msg])
            del cleaned_data['cliente']
            del cleaned_data['cliente_seleccionado_texto']
        if encargado_aux == None:
            msg = 'Debes seleccionar un Encargado'
            self._errors['encargado'] = self.error_class([msg])
            del cleaned_data['encargado']
            del cleaned_data['encargado_seleccionado_texto']
        return cleaned_data