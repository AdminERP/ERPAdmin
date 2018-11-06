from django.contrib import messages
from django.forms import modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from apps.evaluaciones.forms import *
from apps.evaluaciones.models import *
from apps.prueba2.models import Employee


def inicio(request):
    return render(request, 'base.html', {})


def registrar_pregunta(request, id=None):
    pregunta = None
    if id:
        pregunta = get_object_or_404(Question, id=id)

    form = RegistrarPreguntaForm(instance=pregunta)

    if request.method == "POST":
        form = RegistrarPreguntaForm(request.POST, instance=pregunta)
        if form.is_valid():
            form.save()
            messages.success(request, "La pregunta ha sido guardada correctamente.")
            return redirect('consultar_pregunta')
        else:
            messages.error(request, 'Por favor verificar los campos en rojo.')
    return render(request, 'registrar_pregunta.html', {'form': form})


def consultar_pregunta(request):
    return render(request, 'consulta_preguntas.html', {'lista_preguntas': Question.objects.all()})


def desactivar_pregunta(request, id):
    pregunta = get_object_or_404(Question, id=id)
    pregunta.estado = False
    pregunta.save()
    messages.success(request, "La pregunta ha sido desactivada correctamente del sistema")
    return redirect('consultar_pregunta')


def activar_pregunta(request, id):
    pregunta = get_object_or_404(Question, id=id)
    pregunta.estado = True
    pregunta.save()
    messages.success(request, "La pregunta ha sido activado correctamente en el sistema")
    return redirect('consultar_pregunta')


# Evaluations

def registrar_evaluacion(request, id=None):
    evaluacion = get_object_or_404(EmployeeEvaluation, id=id)
    preguntas_evaluacion = evaluacion.employee_evaluation_questions.all()
    cantidad_preguntas_evaluacion = preguntas_evaluacion.count()
    question_formset = modelformset_factory(EmployeeEvaluationQuestions, form=RegistrarPreguntasEnEvaluacionForm,
                                            max_num=cantidad_preguntas_evaluacion, extra=cantidad_preguntas_evaluacion)

    if request.method == "POST":
        formset = question_formset(request.POST, queryset=preguntas_evaluacion)
        if formset.is_valid():
            formset.save()
            messages.success(request, "La evaluacion ha sido guardada correctamente.")
            return redirect('consultar_evaluacion')
        else:
            messages.error(request, 'Por favor verificar los campos en rojo.')
    else:
        formset = question_formset(queryset=preguntas_evaluacion)
    return render(request, 'registrar_evaluaciones.html', {'evaluacion':evaluacion, 'formset': formset, 'preguntas': preguntas_evaluacion})


def creacion_evaluacion(request, id):
    employee = get_object_or_404(Employee, id=id)
    evaluacion = EmployeeEvaluation.objects.create(date=datetime.date.today(),
                                                   employee=employee)
    for pregunta in Question.objects.filter(estado=True):
        EmployeeEvaluationQuestions.objects.create(employeeEvaluationId=evaluacion, questionId=pregunta, score=0,
                                                   observation='')
    return redirect('registrar_evaluacion', evaluacion.id)


def consultar_evaluacion(request):
    return render(request, 'consulta_evaluaciones.html', {'lista_evaluaciones': EmployeeEvaluation.objects.all()})


def desactivar_evaluacion(request, id):
    evaluacion = get_object_or_404(Question, id=id)
    evaluacion.estado = False
    evaluacion.save()
    messages.success(request, "La evaluacion ha sido desactivada correctamente del sistema")
    return redirect('consultar_evaluacion')


def activar_evaluacion(request, id):
    evaluacion = get_object_or_404(Question, id=id)
    evaluacion.estado = True
    evaluacion.save()
    messages.success(request, "La evaluacion ha sido activado correctamente en el sistema")
    return redirect('consultar_evaluacion')
