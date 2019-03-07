from django import forms
from django.contrib.auth.forms import UserCreationForm
from apps.usuarios.models import *


class CrearUsuarioForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'fecha_nacimiento', 'cedula', 'telefono', 'email', 'direccion',
                  'estado_civil', 'password1', 'password2', 'is_active')

    def __init__(self, *args, **kwargs):
        super(CrearUsuarioForm, self).__init__(*args, **kwargs)

        for fieldname in ['password1', 'password2', 'is_active']:
            self.fields[fieldname].help_text = None


class EditarUsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'fecha_nacimiento', 'cedula', 'telefono', 'email', 'direccion',
                  'estado_civil','is_active')

    def __init__(self, *args, **kwargs):
        super(EditarUsuarioForm, self).__init__(*args, **kwargs)

        for fieldname in ['is_active']:
            self.fields[fieldname].help_text = None

class CrearClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
