from django import forms
from apps.inventario.models import *

class RegistroEntrada(forms.ModelForm):

	class Meta:
		model = Entrada
		fields = {"condicion", "razon_devolucion", "fecha", "ordenCompra"}
		labels = {
			'condicion': 'Condición de llegada',
            'razon_devolucion': 'Razón de devolución',
            'fecha': 'Fecha de entrada',
            'ordenCompra': 'Orden de compra',
        }
		widgets = {
			'fecha': forms.DateInput(attrs={'class':'datepicker'}),
		}
	def __init__(self, *args, **kwargs):
		super(RegistroEntrada, self).__init__(*args, **kwargs)
		self.fields['ordenCompra'].widget.attrs['disabled'] = True
