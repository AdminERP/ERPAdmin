from django import forms

from apps.employees_and_jobs.models import Job
from apps.employees_and_jobs.models import Employee


class RegistrarCargoForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['name', 'description', 'functions', 'has_vacants']


class RegisterEmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'id_type', 'identification', 'address', 'email', 'telephone', 'eps', 'pension_fund',
                  'severance_fund', 'bank', 'account_number', 'salary', 'cargo', 'jefe', 'status']
