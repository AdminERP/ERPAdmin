# Django
from django.views.generic import ListView

# App Models
from apps.datosmaestros.models import (
    CategoriaModel,
    DatoModel,
    ValorModel
)

class ValorListView(ListView):
    """Listar todos los valores."""
    model = ValorModel
    context_object_name = 'valores'
    template_name = 'datosmaestros/valor_listar.html'

    def get_queryset(self):
        """
        Sobrescribimos la funcion 'get_queryset' para
        filtrar los valores de determinado dato
        y para incluir dicho dato y su categoria
        en el contexto.
        """
        id_categoria = self.kwargs['id_categoria']
        id_dato = self.kwargs['id_dato']
        self.extra_context = {
            'categoria': CategoriaModel.objects.get(id = id_categoria),
            'dato': DatoModel.objects.get(id = id_dato)
        }
        return ValorModel.objects.filter(dato = id_dato)
