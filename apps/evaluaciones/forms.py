from django import forms

from apps.evaluaciones.models import EmployeeEvaluation, Question, EmployeeEvaluationQuestions


class RegistrarPreguntaForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_statement']

'''
class RegistrarEvaluacionForm(forms.ModelForm):
    class Meta:
        model = EmployeeEvaluation
        fields = ['employee']
'''


class RegistrarPreguntasEnEvaluacionForm(forms.ModelForm):
    PUNTAJES_CHOICES = ((0, '0'),
                        (1, '1'),
                        (2, '2'),
                        (3, '3'),
                        (4, '4'),
                        (5, '5'))
    score = forms.ChoiceField(choices=PUNTAJES_CHOICES, widget=forms.RadioSelect())
    class Meta:
        model = EmployeeEvaluationQuestions
        fields = ['score', 'observation']