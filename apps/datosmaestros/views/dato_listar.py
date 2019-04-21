# Django
from django.views.generic import ListView

# App Models
from apps.datosmaestros.models import DatoModel, CategoriaModel

class DatoListView(ListView):
    """Listar todos los datos."""
    model = DatoModel
    context_object_name = 'datos'
    template_name = 'datosmaestros/dato_listar.html'

    def get_queryset(self):
        """
        Sobrescribimos la funcion 'get_queryset' para
        filtrar los datos de determinada catergoria
        y para incluir dicha categoria en el contexto.
        """
        id_categoria = self.kwargs['id_categoria']
        self.extra_context = {
            'categoria': CategoriaModel.objects.get(id = id_categoria)
        }
        return DatoModel.objects.filter(categoria = id_categoria)
