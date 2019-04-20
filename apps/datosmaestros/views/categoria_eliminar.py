# Django
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.http.response import JsonResponse

# App Models
from apps.datosmaestros.models import CategoriaModel

class CategoriaDeleteView(DeleteView):
    """Eliminar una categoria."""
    def delete(self, request, *args, **kwargs):
        """
        Sobrescribimos la funcion 'delete' para realizar
        un borrado logico en el sistema ERP.

        La funcion es definida para manejar una petición
        de tipo AJAX.
        """
        id = request.POST['id']
        categoria = CategoriaModel.objects.get(id = id)
        categoria.estado = not categoria.estado
        if categoria.estado:
            messages.success(
                self.request,
                '¡Categoría activada exitosamente!'
            )
        else:
            messages.success(
                self.request,
                '¡Categoría desactivada exitosamente!'
            )
        categoria.save()
        data = {
            'url': reverse_lazy('datosmaestros:listar_categorias')
        }
        return JsonResponse(data)
