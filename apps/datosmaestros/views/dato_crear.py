# Django
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView

# App Forms
from apps.datosmaestros.forms import DatoForm

# App Models
from apps.datosmaestros.models import CategoriaModel, DatoModel

class DatoCreateView(CreateView):
    """Crea un dato."""
    form_class = DatoForm
    template_name = 'datosmaestros/dato_crear.html'

    def get_success_url(self):
        """
        Sobrescribimos la funcion 'get_success_url'
        para incluir la categoria de los datos en la url.
        """
        return reverse_lazy('datosmaestros:listar_datos', kwargs = {
            'id_categoria': self.kwargs['id_categoria']
        })

    def get_context_data(self, **kwargs):
        """
        Sobrescribimos la funcion 'get_context_data'
        para incluir la categoria en el contexto.
        """
        context = super(DatoCreateView, self).get_context_data(**kwargs)
        context['id_categoria'] = self.kwargs['id_categoria']
        return context

    def form_valid(self, form):
        """
        Sobrescribimos la funcion 'form_valid' para
        agregar soporte a notificaciones.
        """
        dato = form.save()
        dato.categoria = CategoriaModel.objects.get(id = self.kwargs['id_categoria'])
        dato.save()

        messages.success(
            self.request,
            '¡Dato creado exitosamente!'
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Sobrescribimos la funcion 'form_invalid' para
        agregar soporte a notificaciones.
        """
        messages.error(
            self.request,
            'Por favor corrige los errores'
        )
        return super().form_invalid(form)
