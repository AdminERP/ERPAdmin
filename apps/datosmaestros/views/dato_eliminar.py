# Django
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.http.response import JsonResponse

# App Models
from apps.datosmaestros.models import DatoModel

class DatoDeleteView(DeleteView):
    """Eliminar un dato."""
    def delete(self, request, *args, **kwargs):
        """
        Sobrescribimos la funcion 'delete' para realizar
        un borrado logico en el sistema ERP.

        La funcion es definida para manejar una petición
        de tipo AJAX.
        """
        id = request.POST['id']
        dato = DatoModel.objects.get(id = id)
        dato.estado = not dato.estado
        if dato.estado:
            messages.success(
                self.request,
                '¡Dato activado exitosamente!'
            )
        else:
            messages.success(
                self.request,
                '¡Dato desactivado exitosamente!'
            )
        dato.save()
        data = {
            'url': reverse_lazy(
                'datosmaestros:listar_datos',
                kwargs = {
                    'id_categoria': self.kwargs['id_categoria']
                }
            )
        }
        return JsonResponse(data)
