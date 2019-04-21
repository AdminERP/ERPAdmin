# Django
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.http.response import JsonResponse

# App Models
from apps.datosmaestros.models import ValorModel

class ValorDeleteView(DeleteView):
    """Eliminar un valor."""
    def delete(self, request, *args, **kwargs):
        """
        Sobrescribimos la funcion 'delete' para realizar
        un borrado logico en el sistema ERP.

        La funcion es definida para manejar una petición
        de tipo AJAX.
        """
        id = request.POST['id']
        valor = ValorModel.objects.get(id = id)
        valor.estado = not valor.estado
        if valor.estado:
            messages.success(
                self.request,
                '¡Valor activado exitosamente!'
            )
        else:
            messages.success(
                self.request,
                '¡Valor desactivado exitosamente!'
            )
        valor.save()
        data = {
            'url': reverse_lazy(
                'datosmaestros:listar_valores',
                kwargs = {
                    'id_categoria': self.kwargs['id_categoria'],
                    'id_dato': self.kwargs['id_dato']
                }
            )
        }
        return JsonResponse(data)
