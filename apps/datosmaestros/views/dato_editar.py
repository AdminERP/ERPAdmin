# Django
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import UpdateView

# App Forms
from apps.datosmaestros.forms import DatoForm

# App Models
from apps.datosmaestros.models import CategoriaModel, DatoModel


class DatoUpdateView(UpdateView):
    """Editar un dato."""
    model = DatoModel
    pk_url_kwarg = 'id_dato'
    form_class = DatoForm
    template_name = 'datosmaestros/dato_editar.html'

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
        context = super(DatoUpdateView, self).get_context_data(**kwargs)
        context['id_categoria'] = self.kwargs['id_categoria']
        return context

    def form_valid(self, form):
        """
        Sobrescribimos la funcion 'form_valid' para
        agregar soporte a notificaciones.
        """
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
