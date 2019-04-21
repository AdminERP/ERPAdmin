# Django
from django import forms

# App Models
from apps.datosmaestros.models import DatoModel

class DatoForm(forms.ModelForm):
    """
    DatoForm define la estructura del formulario
    para crear y editar instancias de DatoModel.
    """
    class Meta:
        model = DatoModel
        fields = ('nombre', 'descripcion', 'tipo')
