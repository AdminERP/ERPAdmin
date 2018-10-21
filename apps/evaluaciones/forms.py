from django import forms

from apps.evaluaciones.models import Question


class RegistrarPreguntaForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_statement']