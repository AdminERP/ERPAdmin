# Django
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView

# App Forms
from apps.datosmaestros.forms import CategoriaForm

class CategoriaCreateView(CreateView):
    """Crea una categoria."""
    form_class = CategoriaForm
    success_url = reverse_lazy('datosmaestros:listar_categorias')
    template_name = 'datosmaestros/categoria_crear.html'

    def form_valid(self, form):
        """
        Sobrescribimos la funcion 'form_valid' para
        agregar soporte a notificaciones.
        """
        messages.success(
            self.request,
            '¡Categoría creada exitosamente!'
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
