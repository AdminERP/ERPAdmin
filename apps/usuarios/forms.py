from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django_select2.forms import Select2Widget, Select2MultipleWidget
from apps.usuarios.models import *


class CrearUsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ('first_name', 'last_name', 'cedula', 'username', 'cargo', 'password1', 'password2',
                  'fecha_nacimiento', 'telefono', 'email', 'direccion', 'estado_civil', 'is_active')
        widgets = {
            'fecha_nacimiento': forms.TextInput(attrs={'data-inputmask': "'alias': 'dd/mm/yyyy'", 'data-mask': ''}),
            'cargo': Select2Widget(),
            'estado_civil': Select2Widget()
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
        widgets = {
            'permissions': Select2MultipleWidget(),
            'descripcion': forms.Textarea(attrs={'rows': 2})
        }
        labels = {
            'descripcion': 'Descripción'
        }
        help_texts = {
            'descripcion': 'Escriba una breve descripción del cargo.',
        }


class EditarPasswordForm(PasswordChangeForm):
        def __init__(self, *args, **kwargs):
            super(EditarPasswordForm, self).__init__(*args, **kwargs)
            self.fields['new_password1'].help_text = None
