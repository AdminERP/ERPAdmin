# Django
from django.views.generic import ListView

# App Models
from apps.datosmaestros.models import CategoriaModel

class CategoriaListView(ListView):
    """Listar todas las categorias."""
    model = CategoriaModel
    context_object_name = 'categorias'
    template_name = 'datosmaestros/categoria_listar.html'
