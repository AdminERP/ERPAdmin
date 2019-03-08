from django import forms
from django.contrib.auth.forms import UserCreationForm
from apps.usuarios.models import *


class CrearUsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ('first_name', 'last_name', 'cedula', 'username', 'cargo', 'password1', 'password2',
                  'fecha_nacimiento', 'telefono', 'email', 'direccion', 'estado_civil', 'is_active')
        widgets = {
            'fecha_nacimiento': forms.TextInput(attrs={'data-inputmask': "'alias': 'dd/mm/yyyy'", 'data-mask': ''})
        }

    def __init__(self, *args, **kwargs):
        super(CrearUsuarioForm, self).__init__(*args, **kwargs)

        for fieldname in ['password1', 'password2', 'is_active']:
            self.fields[fieldname].help_text = None


class EditarUsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('first_name', 'last_name', 'username', 'fecha_nacimiento', 'cedula', 'telefono', 'email', 'direccion',
                  'estado_civil', 'is_active', 'cargo')

    def __init__(self, *args, **kwargs):
        super(EditarUsuarioForm, self).__init__(*args, **kwargs)

        for fieldname in ['is_active']:
            self.fields[fieldname].help_text = None


class CrearCargoForm(forms.ModelForm):
    class Meta:
        model = Cargo
        fields = ('name', 'descripcion', 'permissions')
