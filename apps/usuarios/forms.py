import datetime
import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django_select2.forms import Select2Widget, Select2MultipleWidget

from apps.usuarios.models import *


class CrearUsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ('first_name', 'last_name', 'cedula', 'username', 'cargo', 'password1', 'password2',
                  'fecha_nacimiento', 'telefono', 'email', 'direccion', 'estado_civil', 'is_active',
                  'eps', 'pension_fund', 'severance_fund', 'bank', 'account_number', 'salary', 'jefe')
        widgets = {
            'cargo': Select2Widget(),
            'estado_civil': Select2Widget(),
            'jefe': Select2Widget(),
        }

    def __init__(self, *args, **kwargs):
        super(CrearUsuarioForm, self).__init__(*args, **kwargs)

        for fieldname in ['password1', 'password2', 'is_active', 'username']:
            self.fields[fieldname].help_text = None

    def clean_nombre(self):
        nombre = self.cleaned_data['first_name']
        regex_nombre = re.compile('^[a-zA-Z áéíóúñÑ\\s]{3,80}$', re.IGNORECASE)
        if not regex_nombre.match(nombre):
            self.add_error('first_name', 'Nombre debe ser mayor a 3 caracteres y a-z')
        return self.cleaned_data['first_name']

    def clean_apellido(self):
        apellido = self.cleaned_data['last_name']
        regex_nombre = re.compile('^[a-zA-Z áéíóúñÑ\\s]{3,80}$', re.IGNORECASE)
        if not regex_nombre.match(apellido):
            self.add_error('last_name', 'Apellido debe ser mayor a 3 caracteres y a-z')
        return self.cleaned_data['last_name']

    def clean_telefono(self):
        telefono = self.cleaned_data['telefono']
        regex_telefono = re.compile('^[0-9]{7,11}$')
        if not regex_telefono.match(telefono):
            self.add_error('telefono', 'Teléfono deber ser entre 7 y 11 números')
        return self.cleaned_data['telefono']

    def clean_fecha_nacimiento(self):
        # Validacion de fecha de nacimiento
        try:
            fecha_nacimiento = self.cleaned_data['fecha_nacimiento']
            # Valida que la fecha ingresada sea de hace 18 años minimo
            if fecha_nacimiento + datetime.timedelta(weeks=937) > datetime.date.today():
                self.add_error('fecha_nacimiento', 'Ingrese una fecha válida')
        except KeyError:
            self.add_error('fecha_nacimiento', 'Formato de fecha inválido, deberia ser DD/MM/YYYY')
        # Fin validacion fecha nacimiento
        return self.cleaned_data['fecha_nacimiento']


class EditarUsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('first_name', 'last_name', 'username', 'fecha_nacimiento', 'cedula', 'telefono', 'email', 'direccion',
                  'estado_civil', 'is_active', 'cargo', 'eps', 'pension_fund', 'severance_fund', 'bank', 'account_number', 'salary', 'jefe')
        widgets = {
            'cargo': Select2Widget(),
            'estado_civil': Select2Widget(),
            'jefe': Select2Widget(),
        }

    def __init__(self, *args, **kwargs):
        super(EditarUsuarioForm, self).__init__(*args, **kwargs)

        for fieldname in ['is_active', 'username']:
            self.fields[fieldname].help_text = None

    def clean_nombre(self):
        nombre = self.cleaned_data['first_name']
        regex_nombre = re.compile('^[a-zA-Z áéíóúñÑ\\s]{3,80}$', re.IGNORECASE)
        if not regex_nombre.match(nombre):
            self.add_error('first_name', 'Nombre debe ser mayor a 3 caracteres y a-z')
        return self.cleaned_data['first_name']

    def clean_apellido(self):
        apellido = self.cleaned_data['last_name']
        regex_nombre = re.compile('^[a-zA-Z áéíóú\\s]{3,80}$', re.IGNORECASE)
        if not regex_nombre.match(apellido):
            self.add_error('last_name', 'Apellido debe ser mayor a 3 caracteres y a-z')
        return self.cleaned_data['last_name']

    def clean_telefono(self):
        telefono = self.cleaned_data['telefono']
        regex_telefono = re.compile('^[0-9]{7,11}$')
        if not regex_telefono.match(telefono):
            self.add_error('telefono', 'Teléfono deber ser entre 7 y 11 números')
        return self.cleaned_data['telefono']

    def clean_fecha_nacimiento(self):
        # Validacion de fecha de nacimiento
        try:
            fecha_nacimiento = self.cleaned_data['fecha_nacimiento']
            # Valida que la fecha ingresada sea de hace 18 años minimo
            if fecha_nacimiento + datetime.timedelta(weeks=937) > datetime.date.today():
                self.add_error('fecha_nacimiento', 'Ingrese una fecha válida')
        except KeyError:
            self.add_error('fecha_nacimiento', 'Formato de fecha inválido, deberia ser DD/MM/YYYY')
        # Fin validacion fecha nacimiento
        return self.cleaned_data['fecha_nacimiento']


class CrearCargoForm(forms.ModelForm):

    class Meta:
        model = Cargo
        fields = ('name', 'descripcion', 'permissions')
        widgets = {
            'permissions': Select2MultipleWidget(),
            'descripcion': forms.Textarea(attrs={'rows': 2}),
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

        regex_nombre = re.compile('^[a-zA-Z áéíóúñÑ\\s]{3,80}$', re.IGNORECASE)

        if Cargo.objects.filter(name=nombre).exists():
            self.add_error('name', 'Ya existe un cargo con ese nombre')
        if not regex_nombre.match(nombre):
            self.add_error('name', 'Nombre del cargo debe ser mayor a 3 caracteres y a-z')
        if len(descripcion) < 5:
            self.add_error('name', 'Descripción del cargo debe ser mayor a 5 carácteres')

        return self.cleaned_data


class EditarCargoForm(forms.ModelForm):
    temp_id = forms.CharField()

    class Meta:
        model = Cargo
        fields = ('name', 'descripcion', 'permissions', 'temp_id')
        widgets = {
            'permissions': Select2MultipleWidget(),
            'descripcion': forms.Textarea(attrs={'rows': 2}),
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
        temp_id = self.cleaned_data['temp_id']

        regex_nombre = re.compile('^[a-zA-Z áéíóú\\s]{3,80}$', re.IGNORECASE)

        if Cargo.objects.filter(name=nombre).exclude(id=temp_id).exists():
            self.add_error('name', 'Ya existe un cargo con ese nombre')
        if not regex_nombre.match(nombre):
            self.add_error('name', 'Nombre del cargo debe ser mayor a 3 caracteres y a-z')
        if len(descripcion) < 5:
            self.add_error('name', 'Descripción del cargo debe ser mayor a 5 carácteres')

        return self.cleaned_data