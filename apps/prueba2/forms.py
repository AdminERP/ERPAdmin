from django import forms

from apps.prueba2.models import Job
from apps.prueba2.models import Employee


class RegistrarCargoForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['name', 'description', 'functions', 'has_vacants']


class RegisterEmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'id_type', 'identification', 'address', 'email', 'telephone', 'eps', 'pension_fund',
                  'severance_fund', 'bank', 'account_number', 'salary', 'cargo', 'status']
