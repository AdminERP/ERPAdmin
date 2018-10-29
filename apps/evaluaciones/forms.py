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

class HorizontalRadioSelect(forms.RadioSelect):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        css_style = 'style="display: inline-block; margin-right: 10px;"'

        self.renderer.inner_html = '<li ' + css_style + '>{choice_value}{sub_widgets}</li>'

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

