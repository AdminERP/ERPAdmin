from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from apps.evaluaciones.forms import RegistrarPreguntaForm
from apps.evaluaciones.models import Question


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