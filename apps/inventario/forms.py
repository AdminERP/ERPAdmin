from django import forms
from apps.inventario.models import *

class RegistroEntrada(forms.ModelForm):

	class Meta:
		model = Entrada
		fields = {"condicion", "razon_devolucion", "ordenCompra"}
		labels = {
			'condicion': 'Condición de llegada',
            'razon_devolucion': 'Razón de devolución',
            'ordenCompra': 'Orden de compra',
        }
