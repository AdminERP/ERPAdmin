from django import forms

from apps.prueba2.models import Job


class RegistrarCargoForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['name', 'description', 'functions', 'has_vacants']