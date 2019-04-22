# Django
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import UpdateView

# App Forms
from apps.datosmaestros.forms import ValorForm

# App Models
from apps.datosmaestros.models import CategoriaModel, DatoModel, ValorModel

class ValorUpdateView(UpdateView):
    """Editar un valor."""
    model = ValorModel
    pk_url_kwarg = 'id_valor'
    form_class = ValorForm
    template_name = 'datosmaestros/valor_editar.html'

    def get_success_url(self):
        """
        Sobrescribimos la funcion 'get_success_url'
        para incluir la categoria y el dato de los
        valores en la url.
        """
        return reverse_lazy('datosmaestros:listar_valores', kwargs = {
            'id_categoria': self.kwargs['id_categoria'],
            'id_dato': self.kwargs['id_dato']
        })

    def get_context_data(self, **kwargs):
        """
        Sobrescribimos la funcion 'get_context_data'
        para incluir la categoria y el dato en el contexto.
        """
        context = super(ValorUpdateView, self).get_context_data(**kwargs)
        context['id_categoria'] = self.kwargs['id_categoria']
        context['id_dato'] = self.kwargs['id_dato']
        return context

    def form_valid(self, form):
        """
        Sobrescribimos la funcion 'form_valid' para
        agregar soporte a notificaciones.
        """
        messages.success(
            self.request,
            '¡Valor creado exitosamente!'
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
