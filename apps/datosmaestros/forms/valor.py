# Django
from django import forms

# App Models
from apps.datosmaestros.models import ValorModel

class ValorForm(forms.ModelForm):
    """
    ValorForm define la estructura del formulario
    para crear y editar instancias de ValorModel.
    """
    class Meta:
        model = ValorModel
        fields = ('nombre', 'descripcion', 'valor')
