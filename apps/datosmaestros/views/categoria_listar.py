# Django
from django.views.generic import ListView


# App Models
from apps.datosmaestros.models import CategoriaModel

class CategoriaListView(ListView):
    """Listar todas las categorias."""
    model = CategoriaModel
    context_object_name = 'categorias'
    template_name = 'datosmaestros/categoria_listar.html'

    def get_queryset(self):
        queryset = super(ListView, self).get_queryset()
        if not self.request.user.is_superuser:
            queryset = CategoriaModel.objects.filter(
                administrador = self.request.user.cargo
            )
        return queryset
