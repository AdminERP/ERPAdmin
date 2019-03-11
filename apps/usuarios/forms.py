from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django_select2.forms import Select2Widget, Select2MultipleWidget
from apps.usuarios.models import *
import re


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

        for fieldname in ['password1', 'password2', 'is_active', 'username']:
            self.fields[fieldname].help_text = None

    def clean(self):
        nombre = self.cleaned_data['first_name']
        apellido = self.cleaned_data['last_name']
        cedula = self.cleaned_data['cedula']
        username = self.cleaned_data['username']
        correo = self.cleaned_data['email']
        telefono = self.cleaned_data['telefono']

        regex_nombre = re.compile('^[a-zA-ZÁ,\s]{3,20}$', re.IGNORECASE)
        regex_cedula = re.compile('^[0-9]{8,11}$')
        regex_email = re.compile('^(([^<>()\[\],;:\s@"]+(\.[^<>()\[\],;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3'
                                 '}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$')
        regex_telefono = re.compile('^[0-9]{7,11}$')

        if not regex_nombre.match(nombre):
            self.add_error('first_name', 'Nombre debe ser mayor a 3 caracteres y a-z')

        if not regex_nombre.match(apellido):
            self.add_error('last_name', 'Apellido debe ser mayor a 3 caracteres y a-z')

        if not regex_cedula.match(cedula):
            self.add_error('cedula', 'Cédula debe ser numérica entre 8 y 11 números')

        if not regex_email.match(correo):
            self.add_error('email', 'Correo inválido')

        if not regex_telefono.match(telefono):
            self.add_error('telefono', 'Teléfono deber ser entre 7 y 11 números')

        u = Usuario.objects.filter(username=username).count()
        # Si el username esta disponible es True
        if not u == 0:
            self.add_error('username', 'Nombre de usuario no disponible')

        return self.cleaned_data


class EditarUsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('first_name', 'last_name', 'username', 'fecha_nacimiento', 'cedula', 'telefono', 'email', 'direccion',
                  'estado_civil', 'is_active', 'cargo')
        widgets = {
            'fecha_nacimiento': forms.TextInput(attrs={'data-inputmask': "'alias': 'dd/mm/yyyy'", 'data-mask': ''}),
            'cargo': Select2Widget(),
            'estado_civil': Select2Widget()
        }

    def __init__(self, *args, **kwargs):
        super(EditarUsuarioForm, self).__init__(*args, **kwargs)

        for fieldname in ['is_active', 'username']:
            self.fields[fieldname].help_text = None

    def clean(self):
        nombre = self.cleaned_data['first_name']
        apellido = self.cleaned_data['last_name']
        cedula = self.cleaned_data['cedula']
        username = self.cleaned_data['username']
        correo = self.cleaned_data['email']
        telefono = self.cleaned_data['telefono']

        regex_nombre = re.compile('^[a-zA-ZÁ,\s]{3,20}$', re.IGNORECASE)
        regex_cedula = re.compile('^[0-9]{8,11}$')
        regex_email = re.compile('^(([^<>()\[\],;:\s@"]+(\.[^<>()\[\],;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.'
                                 '[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$')
        regex_telefono = re.compile('^[0-9]{7,11}$')

        if not regex_nombre.match(nombre):
            self.add_error('first_name', 'Nombre debe ser mayor a 3 caracteres y a-z')

        if not regex_nombre.match(apellido):
            self.add_error('last_name', 'Apellido debe ser mayor a 3 caracteres y a-z')

        if not regex_cedula.match(cedula):
            self.add_error('cedula', 'Cédula debe ser numérica entre 8 y 11 números')

        if not regex_email.match(correo):
            self.add_error('email', 'Correo inválido')

        if not regex_telefono.match(telefono):
            self.add_error('telefono', 'Teléfono deber ser entre 7 y 11 números')

        return self.cleaned_data


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

    def clean(self):
        nombre = self.cleaned_data['name']
        descripcion = self.cleaned_data['descripcion']

        regex_nombre = re.compile('^[a-zA-ZÁ,\s]{3,80}$', re.IGNORECASE)

        if not regex_nombre.match(nombre):
            self.add_error('name', 'Nombre del cargo debe ser mayor a 3 caracteres y a-z')
        if len(descripcion) < 5:
            self.add_error('name', 'Descripción del cargo debe ser mayor a 5 carácteres')

        return self.cleaned_data


class EditarPasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(EditarPasswordForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].help_text = None
