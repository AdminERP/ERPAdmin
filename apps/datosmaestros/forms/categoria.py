# Django
from django import forms

# App Models
from apps.datosmaestros.models import CategoriaModel

class CategoriaForm(forms.ModelForm):
    """
    CategoriaForm define la estructura del formulario
    para crear y editar instancias de CategoriaModel.
    """
    class Meta:
        model = CategoriaModel
        fields = ('nombre', 'descripcion', 'administrador')
