from django import forms

from .models import CuentaPagar, Item

class PaymentAccountForm(forms.ModelForm):
    class Meta:
        model = CuentaPagar
        fields = (
    		'total',
            'invoice', 
    		'invoice_date',
    		'term_date',
    		'status',
    		'order_id',
    		'supplier_id')

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = (
    		'name', 
    		'value')