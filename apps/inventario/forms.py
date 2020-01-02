from django import forms
from apps.inventario.models import *

class RegistroEntrada(forms.ModelForm):

	class Meta:
		model = Entrada
		fields = {"condicion", "comentario", "ordenCompra"}
		labels = {
			'condicion': 'Condición de llegada',
            'comentario': 'Comentario',
            'ordenCompra': 'Orden de compra',
        }
